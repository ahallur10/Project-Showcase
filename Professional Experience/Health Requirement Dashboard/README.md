# 🩺 Health Requirement Dashboard  

---

## 1. Overview  

> **Figure 1:** Health Requirements Dashboard — Overview (sensitive information blurred)
<img width="1593" height="766" alt="image" src="https://github.com/user-attachments/assets/2434ab0f-925c-42c4-baaf-f570ac244699" />

---
The Health Requirements Dashboard centralizes monitoring of medical and developmental health requirements for Head Start and Early Head Start students. Previously, the health coordinator's relied on multiple ChildPlus reports, re-running filters repeatedly and manually highlighting results which often resulted in working after hours. This dashboard replicates the database validation logic in Power BI and brings all requirements, programs, students and statuses into one place, enabling instant drilldowns by site, program, status, and requirement. 

**Impact:**  
- **Hours → minutes**: monitoring sessions reduced from multi-hour report runs to quick checks.  
- ***80–90%* less manual work**: eliminated repeated report runs or manual tallies/highlighting.
- **Audit-friendly**: Built to match database's generated report numbers and totals, ensuring consistency, accuracy and reliability.

> **Figure 2:** Supply Order Dashboard Detailed Report (sensitive information blurred)
<img width="1702" height="791" alt="image" src="https://github.com/user-attachments/assets/dc57c774-f486-4f1d-aec7-ce616049558f" />

---

## 2. Methodology
This project follows an **ELT workflow**: data extracted from a SQL Server and an Excel file, loaded into Power BI, transformed with Power Query, modeled with clean relationships, and displayed via DAX-driven visuals.

### 🟨🟩 **Extract & Load**

**Summary:**  
The extraction phase required a deep understanding of the source database schema to identify the correct tables and ensure that data aligned with what end users saw in reports and student profiles. This process involved iterative validation that included cross-referencing record counts, field names, and relationships to ensure the resulting dataset accurately reflected health compliance statuses.

Once the relevant entities were identified, the focus shifted to aligning key fields such as the **Program Term** and **Requirement Set** to display only the **current program term’s data**. After verifying these alignments, all necessary tables were loaded into Power BI through secure connections, forming the foundation for the transformation and modeling stages.

---

**Source Systems:**  
- **SQL Server Database** – the core data source containing program participation, student details, and health requirement information.  
- **SharePoint (Custom Event Mapping Table)** – a hosted lookup table linking **Requirement IDs** to readable **Event Names**, created manually to improve consistency and readability.

---

**Data Identification & Validation Steps**

| **Challenge** | **Solution** |
|----------------|--------------|
| **Complex database structure** — The source SQL database contained numerous similarly named tables and views with overlapping columns, making it difficult to identify the correct datasets for students, program participation, health requirements, and health events. | Used a **column-based search** and **cross-referenced ChildPlus-style reports** to pinpoint the correct tables. Verified table relationships by checking sample student records for accuracy. |
| **Unverified data relationships** — Table joins and record counts didn’t initially align with known totals from official reports. | Performed **cross-verification** between extracted data and official program reports/student profiles to ensure one-to-one consistency and eliminate mismatched joins. |
| **Outdated and inactive program terms** — Historical `ProgramTermKey` and `RequirementSetKey` values were present in the database, cluttering visuals with irrelevant records. | Applied targeted filters and adjusted term alignment logic so only the **current program term** is displayed. Excluded inactive terms to improve both accuracy and performance. |
| **Inconsistent event naming conventions** — Backend health requirement IDs did not align with the event names displayed in ChildPlus, causing confusion for coordinators. | Created a **custom “Event Mapping Table”** in Excel and hosted it on **SharePoint** to link `RequirementID` values with user-friendly event names and types. Connected it dynamically to Power BI for continuous updates. |
  
---

### 🟧 **Transform**

**Summary:**  
Once the necessary tables were loaded into Power BI, each dataset underwent a structured transformation process in **Power Query** to ensure data consistency and accurately replicate the logic used by health coordinators in the ChildPlus system. Transformations focused on aligning program terms, normalizing field types, cleaning inconsistent identifiers, and enriching health requirement data with calculated fields for downstream DAX measures.

---

#### Key Transformations

| **Challenge** | **Solution** |
|----------------|--------------|
| **Inconsistent identifiers across tables**: Student and requirement tables used different formats for IDs, which caused join mismatches and missing data. | Standardized all key fields (e.g., `StudentID`, `RequirementID`, `ProgramTermKey`) by converting them to a consistent format. Created combined keys like `StudentTermKey` and `StudentKey` to uniquely match students to their term and health events. |
| **Missing “Status” logic**: The database showed requirement statuses (like *Complete*, *Incomplete*, *Past Due*) on the student profile on the frontent, but these were **not stored in backend tables**. | Reverse-engineered the database's logic, analyzing how dates and requirement periods changed in the reports. Rebuilt this logic in Power BI using calculated **DAX columns** (_see code snippet below_) to accurately mirror ChildPlus’ frontend results. |
| **Incomplete due date calculations**: The backend data didn’t always specify when requirements were due or overdue, making tracking difficult. | Added calculated fields like **`Requirement Period`** in Power Query by combining `AgeRequirement` and `DaysToComplete`. These fields fed into DAX measures such as `Days Until Due`, `Days Elapsed`, and `Past Due Events`. |
| **Large, cluttered tables**: The raw tables contained many unused columns, which slowed down refresh performance. | Selected only relevant columns for analysis (student details, requirement metadata, event dates, and completion logic). This reduced model size and improved refresh speed. |
| **Relationship verification**: Some joins initially produced missing or duplicated results due to key mismatches. | Used Power BI’s **Query Dependencies View** to visually confirm that each dataset connected correctly, ensuring every student and requirement was represented only once. |

---

#### Example Code Snippets

**Main Status Logic**

The following DAX expression was developed to replicate the **status column** shown in the original system’s student profile. It determines whether a health requirement is **complete**, **late**, or **past due** based on event dates and requirement timing rules.

```DAX
Main Status =
VAR HasEvent =
    NOT ISBLANK ( [EventID] )
    && [EventID] <> "00000000-0000-0000-0000-000000000000"

VAR DaysElapsed      = [Days Elapsed (custom)]
VAR DaysUntilDue     = [Days Until Due (custom)]
VAR DaysToCompleteNum = IFERROR ( VALUE ( [DaysToComplete] ), BLANK() )

RETURN
SWITCH (
    TRUE(),
    # Completed but after allowed days
    HasEvent && NOT ISBLANK ( DaysToCompleteNum ) && DaysElapsed > DaysToCompleteNum, "Comp. Late",

    # Completed within allowed timeframe
    HasEvent && ( ISBLANK ( DaysToCompleteNum ) || DaysElapsed <= DaysToCompleteNum ), "Complete",

    # No event and past the due date
    NOT HasEvent && COALESCE ( DaysUntilDue, 0 ) = 0, "Incomplete and Past Due",

    # No event but still within days to complete
    NOT HasEvent && COALESCE ( DaysUntilDue, 0 ) > 0, "Incomplete but not Past Due",

    BLANK()
)
```

**Past Due Events Logic**

To further classify records that are marked as *Incomplete and Past Due*, this calculated column breaks them into two categories:
- **Past Due**: Requirements that have exceeded the allowed completion period.  
- **Past Due but within Days To Complete**: Requirements still technically within the grace period.

```DAX
Past Due Events =
SWITCH (
    TRUE(),

    # Case 1: Fully past due (beyond the allowed completion days)
    [Main Status] = "Incomplete and Past Due"
        && [Days Elapsed (custom)] >= [DaysToComplete Number],
        "Past Due",

    # Case 2: Within grace period (still inside Days To Complete)
    [Main Status] = "Incomplete and Past Due"
        && [Days Elapsed (custom)] < [DaysToComplete Number],
        "Past Due but within Days To Complete",

    -- Default case: all other records
    BLANK()
)
```
**Example PowerQuery Transformation**

The following script cleans, enriches, and standardizes raw health requirement data. It joins requirement metadata, adds a custom **Requirement Period** column, merges event mapping details from SharePoint, and outputs a simplified table ready for modeling.
```m
let
    Source = Sql.Database("<SERVER>"),
    RawTable = Source{[Schema="dbo", Item="Health_Reqs_Cache"]}[Data],

    # Select necessary columns
    Selected = Table.SelectColumns(RawTable, {"StudentID", "RequirementID", "ProgramTerm_ID", "DaysToComplete"}),

    # Merge with Requirement metadata
    Merged = Table.NestedJoin(Selected, {"RequirementID"}, Health_Requirement, {"RequirementID"}, "RequirementMeta", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "RequirementMeta", {"RequirementName", "AgeRequirement"}),

    # Add calculated logic field
    AddedPeriod = Table.AddColumn(Expanded, "Requirement Period", each if [AgeRequirement] = true then "Due at Age" else "Days To Complete"),

    # Merge with SharePoint mapping table
    MergedMapping = Table.NestedJoin(AddedPeriod, {"RequirementID"}, Event_Mapping_Table, {"RequirementID"}, "Mapping", JoinKind.LeftOuter),
    ExpandedMapping = Table.ExpandTableColumn(MergedMapping, "Mapping", {"EventName", "EventType"}),

    # Clean up and finalize
    Cleaned = Table.SelectColumns(ExpandedMapping, {"StudentID", "EventName", "Requirement Period", "ProgramTermKey"})
in
    Cleaned
```
---


