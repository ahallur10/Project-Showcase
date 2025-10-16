# 📦 Supply Order Dashboard  

---

## 1. Overview  

*(Insert dashboard screenshot here — ideally a clean, full-view image of your main report page)*  
> **Figure 1:** Supply Order Dashboard Overview  

The Supply Order Dashboard was developed to streamline and centralize how classroom supply requests are tracked and analyzed across all Head Start sites.  
Before this project, the process relied on manual spreadsheets and ad-hoc reports, leading to inconsistent data, duplicate entries, and delayed visibility into spending patterns.  

This dashboard automated the entire reporting workflow, provided a single source of truth for supply data, and enabled supervisors to quickly identify fulfillment trends, item demand, and site-level procurement activity.  

**Impact:**  
- Reduced report generation time from hours to minutes.  
- Improved accuracy across 60+ classroom sites.  
- Enhanced purchasing decisions with real-time insights into supply usage and spending trends.  

---

## 2. Methodology  

The dataset was sourced from SQL Server and Excel reference files.  
I used **Power Query** within Power BI to connect, clean, and normalize the data before modeling it in a star schema for dashboard use.  

The key transformation stages included:  
- Cleaning and filtering raw order data.  
- Unpivoting wide-format tables into long-form structures.  
- Merging mappings for category standardization.  
- Creating dimension tables for site, category, and time.  
- Building relationships and DAX measures for analysis.  

Below are two key visuals that illustrate this process:  

1. **Transformation Steps Diagram** — outlines how raw data flows through each ETL stage.  
2. **Query Dependencies Diagram** — visualizes table connections and lineage within the Power BI model.  

*(Insert both diagrams here — labeled Figure 2 and Figure 3)*  

---

## 3. Tables Used  

| **Table Name** | **Purpose** |
|----------------|-------------|
| `vClassroomSupplyOrders` | Main fact table containing all classroom supply requests. |
| `Classroom_Mapping` | Maps item codes to standardized category names. |
| `Site` | Provides site-level details including region and program. |
| `ActiveSites` | Filters active classrooms for inclusion in reporting. |
| `vw_SupplyDashboardView` | Aggregated output feeding visuals in the dashboard. |
| `Dim_Date` | Calendar table for time-based metrics and trends. |
| `Dim_ItemCategory` | Groups items by category and subcategory. |

*(Add or remove rows as needed — keep concise but representative.)*  

---

## 4. Future Iterations  

- Integrate **inventory tracking** to analyze stock levels vs requests.  
- Enable **automated data refresh** for real-time insights.  
- Add **drill-through reports** for site-level expenditure tracking.  
- Explore integration with **procurement systems** for predictive ordering.  

---
placeholder
