# 📦 Supply Order Dashboard  

---

## 1. Overview  

> **Figure 1:** Supply Order Dashboard Overview Report (sensitive information blurred)
<img width="1701" height="680" alt="image" src="https://github.com/user-attachments/assets/7d9cab1c-499e-4076-896e-5a48a561d8e0" />


The Supply Order Dashboard was developed to streamline and centralize how supply order requests are tracked and analyzed across all Head Start sites and classrooms. Before this project, the process relied on manual spreadsheets and ad-hoc reports, leading to inconsistent data, duplicate entries, and delayed visibility into spending patterns. This dashboard automated the entire reporting workflow, provided a single source of truth for supply data, and enabled supervisors to quickly identify fulfillment trends, item demand, and site-level activity.  

**Impact:**  
- Reduced report generation time from hours to minutes.  
- Improved accuracy across 60+ sites.  
- Enhanced purchasing decisions with real-time insights into supply usage and spending trends.  

> **Figure 2:** Supply Order Dashboard Detailed Report (sensitive information blurred)
<img width="1603" height="831" alt="image" src="https://github.com/user-attachments/assets/934f4435-561b-4096-8e6b-64c832c8d88f" />

---

## 2. Methodology  

The following section outlines the end-to-end data pipeline used to build the Supply Orders Dashboard.  
This project follows an **ELT (Extract → Load → Transform)** workflow, where data is sourced from SQL Server, loaded into Power BI and transformed via Power Query before visualization.

---

### 🟨🟩 **Extract & Load**

**Summary:**  
The data extraction process involved identifying and connecting to the correct SQL Server tables, as the source tables used non-intuitive naming conventions (e.g., `Table853`). A column-based search approach was used to locate the relevant supply order datasets across the database.  

**Source:**  
- SQL Server Database (configured through a secure VPN tunnel)

**Extracted Tables:**  
- Classroom Supply Orders  
- Office Supply Orders  
- Janitorial/PPE Supply Orders  
- Diapering Supply Orders  
- Site (location metadata)  

**Extraction Method:**  
- Connected to the SQL Server via Power BI’s **SQL Database Connector**  
- Initial SQL queries were refined to optimize performance and minimize compute usage during scheduled refreshes  
- Supplementary custom **Mapping Sheets** were created and maintained in SharePoint, connected through the **Sharepoint Connector** for dynamic refreshes

---

### 🟧 **Transform**

**Summary**

After loading the tables into Power BI, each dataset underwent a structured transformation process within **Power Query** to standardize, clean, and prepare the data for analysis. On average, each table contained 15–19 applied steps, following a consistent workflow across all supply order types.

---

**Key Transformation Steps:**

- **Challenge and Solution: Custom Mapping Creation**

  Since the backend tables lacked category fields and contained inconsistent item names (e.g., `Black_203` and `Black_320` referring to similar items), a custom **mapping sheet** was created for each supply order type.  
  - These mapping sheets linked raw item names to standardized **categories** and **display names**, aligning backend data with the frontend order forms.  
  - The mappings were maintained in SharePoint and connected to Power BI for dynamic updates.  
  - **Limitation:** Any new or renamed items required manual updates to the mapping sheet and corresponding query adjustments (see *Suggested Improvements* section for future automation ideas).

- **Data Standardization and Cleaning**

  Each table’s transformation included:
  - Unpivoting wide item columns into a long format (`Item`, `Quantity`)  
  - Merging with custom mapping tables to enrich data with categories and item names  
  - Joining with the `Site` table to include location and program context  
  - Replacing null or blank values with defaults and filtering out deleted records  
  - Duplicating key identifiers (`ClusterID`) and renaming columns for uniformity  
  - Adding a `Source` field for data lineage tracking  

---

**Example Transformation (Simplified Power Query M):**  
The snippet below illustrates a summarized version of the transformation process for one supply order table. A similar transforming method was created for all the other tables.

```m
let
    --- EXTRACT ---
    Source = Sql.Database("<SERVER_NAME>"),
    Database = Source{[Name="<DATABASE_NAME>"]}[Data],
    RawTable = Database{[Schema="dbo", Item="SupplyOrder1"]}[Data],

    --- LOAD ---
    SelectedColumns = Table.SelectColumns(RawTable, {"LocationID", "Status", "ClusterID", "Item_1", ..., "Item_25"}),

    --- TRANSFORM ---
    1. Unpivoted = Table.Unpivot(SelectedColumns, {"Item_1", ..., "Item_25"}, "Item_Code", "Quantity"),
    2. Merged Mapping = Table.NestedJoin(Unpivoted, {"Item_Code"}, Item_Mapping, {"Item_Code"}, "Mapping", JoinKind.LeftOuter),
    3. Expanded Mapping = Table.ExpandTableColumn(MergedMapping, "Mapping", {"Category", "Item_Name"}, {"Category", "Item"}),
    4. Merged Site = Table.NestedJoin(ExpandedMapping, {"LocationID"}, Site, {"SiteID"}, "Site", JoinKind.LeftOuter),
    5. Expanded Site = Table.ExpandTableColumn(MergedSite, "Site", {"SiteName"}, {"Site"}),
    6. Cleaned = Table.ReplaceValue(ExpandedSite, "", "Blank", Replacer.ReplaceValue, {"Status"}),
    7. Filtered = Table.SelectRows(Cleaned, each ([DeleteDate] = null)),
    8. AddedSource = Table.AddColumn(Filtered, "Source", each "Supply Orders"),
    9. DuplicatedID = Table.DuplicateColumn(AddedSource, "ClusterID", "Supply Order Number"),
    10. Renamed = Table.RenameColumns(DuplicatedID, {{"Item_Code", "Item (Raw)"}, {"Status", "Order Status"}}),
    11. Final Types = Table.TransformColumnTypes(Renamed, {{"Supply Order Number", type text}})
in
    FinalTypes
```

This transformation pipeline standardized the raw supply data into a unified, analysis-ready format.

---

### 🟦 **Model & Visualize**

**Summary:**  
All supply order tables were appended into a unified `Overview Table`, serving as the primary fact table for the dashboard. Two calculated DAX columns were added to identify orders with zero quantities and flag them for quality checks.

**Example DAX (Simplified) for flagging supply orders with no items:**
```m
No_Items =
VAR CurrentOrder = 'SupplyOrders'[OrderID]
VAR TotalQuantity =
    CALCULATE (
        SUM ( 'SupplyOrders'[Quantity] ),
        FILTER (
            'SupplyOrders',
            'SupplyOrders'[OrderID] = CurrentOrder
        )
    )
RETURN
    IF (TotalQuantity = 0, 1, 0)
```
**Visualization Design:**

- Created an Overview Report for a holistic view of all supply order types.
- Designed individual reports for each order category with drill-down filters.
- Built 40+ DAX measures to maintain consistency across cards, matrices, and charts.

**Deployment:**

- Built and refreshed within a secured virtual machine (VM) due to database access restrictions.
- Configured an on-premises data gateway for automated refreshes after publishing to the Power BI workspace.

---

### 📈 **Diagrams**

Below are two key visuals that illustrate this process:  

> **Transformation Steps Diagram:** _outlines how raw data flows through each ETL stage_ 
<img width="1745" height="1544" alt="image" src="https://github.com/user-attachments/assets/3c99d0bf-6cf4-4173-9181-052e8b728d4e" />

> **Figure 2:** Query Dependencies Diagram _visualizes table connections and lineage within the Power BI model_

---

## 3. Tables Used  

| **Table Name(s)** | **Purpose** |
|-------------------|-------------|
| `Classroom Supply Orders`, `Office Supply Orders`, `Janitorial/PPE Supply Orders`, `Diapering Supply Orders` | Core fact tables extracted from SQL Server. Each represents a different supply category, later unpivoted, cleaned, and merged into a unified dataset. |
| `Classroom_Mapping`, `Office_Mapping`, `Janitorial_Mapping`, `Diapering_Mapping` | Lookup (dimension) tables providing standardized item names and categories for each supply type. Used in Power Query transformations for consistent labeling and grouping. |
| `Site` | Dimension table containing site-level information such as name, program, and region, used for location or program-based filtering. |
| `Overview Table` | Consolidated output table combining all supply order types after transformation. Serves as the main source for the Power BI dashboard visuals on the Overview report. |

---

## 4. Future Iterations  

- Integrate **inventory tracking** to analyze stock levels vs requests.  
- Enable **automated data refresh** for real-time insights.  
- Add **drill-through reports** for site-level expenditure tracking.  
- Explore integration with **procurement systems** for predictive ordering.  

---
placeholder
