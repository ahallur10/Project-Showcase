# 🩺 Health Requirement Dashboard  

---

## 1. Overview  

> **Figure 1:** Health Requirements Dashboard — Overview (sensitive information blurred)
<img width="1593" height="766" alt="image" src="https://github.com/user-attachments/assets/2434ab0f-925c-42c4-baaf-f570ac244699" />

---
The Health Requirements Dashboard centralizes monitoring of medical and developmental health requirements for Head Start and Early Head Start students. Previously, the health coordinators relied on multiple ChildPlus reports, re-running filters repeatedly and manually highlighting results which often resulted in working after hours. This dashboard replicates the database validation logic in Power BI and brings all requirements, programs, students and statuses into one place, enabling instant drilldowns by site, program, status, and requirement. 

**Impact:**  
- **Hours → minutes**: monitoring reduced from multi-hour report runs to quick checks.  
- **Audit-friendly**: Built to match official report totals for consistency and reliability.
- ***80–90%* less manual work**: no repeated report runs or manual highlighting.

> 💡 **Impact Snapshot**
> 
> | **Before** | **After** |
> |-------------|------------|
> | Manually run reports, repeated filter runs, and manual highlighting (2–3 hrs/day) | Instant monitoring and drilldowns in Power BI (10–15 mins/day) |
> 
> **Conservative Estimated Time Saved:** 1.5–2.5 hours per day → **30–50 hours per month**

---

> **Figure 2:** Health Requirements Dashboard — Detailed View (sensitive information blurred)
<img width="1702" height="791" alt="image" src="https://github.com/user-attachments/assets/dc57c774-f486-4f1d-aec7-ce616049558f" />

---

## 2. Methodology
This project follows an **ELT workflow**: **Extract** data from SQL Server and a SharePoint-hosted Excel lookup, **Load** into Power BI, then **Transform** with Power Query and DAX before modeling and visualization.

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
| **Complex database structure** — The source SQL database contained numerous similarly named tables and views with overlapping columns, making it difficult to identify the correct datasets for students, program participation, health requirements, and health events. | Used a **column-based search** and **cross-referenced live reports** to pinpoint the correct tables. Verified table relationships by checking sample student records for accuracy. |
| **Unverified data relationships** — Table joins and record counts didn’t initially align with known totals from official reports. | Performed **cross-verification** between extracted data and official program reports/student profiles to ensure one-to-one consistency and eliminate mismatched joins. |
| **Outdated and inactive program terms** — Historical `ProgramTermKey` and `RequirementSetKey` values were present in the database, cluttering visuals with irrelevant records. | Applied targeted filters and adjusted term alignment logic so only the **current program term** is displayed. Excluded inactive terms to improve both accuracy and performance. |
| **Inconsistent event naming conventions** — Backend health requirement IDs did not align with the event names displayed in ChildPlus, causing confusion for coordinators. | Created a **custom “Event Mapping Table”** in Excel and hosted it on **SharePoint** to link `RequirementID` values with user-friendly event names and types. Connected it dynamically to Power BI for continuous updates. |
  
---

### 🟧 **Transform**

**Summary:**  
After loading the necessary tables, each dataset was standardized in **Power Query** and aligned to the **current program term**. A key challenge was that requirement **statuses are not stored in backend tables** as they were computed by the original system’s frontend. I independently reverse-engineered this logic without access to vendor documentation or support, validating my results against live reports to ensure perfect alignment.

---

### Key Transformations

| **Challenge** | **Solution** |
|---|---|
| **Inconsistent identifiers across tables** caused join mismatches. | Standardized key fields (e.g., `StudentID`, `RequirementID`, `ProgramTermKey`) and created composite keys (`StudentTermKey`, `StudentKey`) for unique, reliable joins. |
| **Missing “Status” logic** — the system displays statuses (Complete, Incomplete, Past Due) on the frontend, but they aren’t persisted in the backend. | Reverse-engineered the rules via report/profile comparisons and rebuilt them as DAX calculations (see `Main Status` below) to exactly match official outputs. |
| **Incomplete due date logic** — due/overdue semantics weren’t explicit in raw data. | Derived **Requirement Period** in Power Query from `AgeRequirement` and `DaysToComplete`; fed that into DAX (`Days Until Due`, `Days Elapsed`, `Past Due Events`). |
| **Large, cluttered tables** slowed refreshes. | Selected only analysis-relevant columns (student, requirement metadata, event dates, completion logic) to trim model size and speed refresh. |


---

## Example Code Snippets

**Main Status Logic**

As mentioned previously, status values weren't stored in the backend, which involved reverse-engineering the logic that the database used. The following DAX expression was developed to replicate the **status column** shown in the original system’s student profile. It determines whether a health requirement is **complete**, **late**, or **past due** based on event dates and requirement timing rules.

```DAX
Main Status =
VAR HasEvent =
    NOT ISBLANK ( [EventID] )
    && [EventID] <> "00000000-0000-0000-0000-000000000000"

VAR DaysElapsed      = [Days Elapsed (custom)]
VAR DaysUntilDue     = [Days Until Due (custom)]
VAR DaysToComplete (custom) = IFERROR ( VALUE ( [DaysToComplete] ), BLANK() )

RETURN
SWITCH (
    TRUE(),
    # Completed but after allowed days
    HasEvent && NOT ISBLANK ( DaysToComplete (custom) ) && DaysElapsed > DaysToComplete (custom), "Comp. Late",

    # Completed within allowed timeframe
    HasEvent && ( ISBLANK ( DaysToComplete (custom) ) || DaysElapsed <= DaysToComplete (custom) ), "Complete",

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
    Selected = Table.SelectColumns(RawTable, {"StudentID", "RequirementID", "ProgramTermKey", "DaysToComplete"}),

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

## 📈 Data Flow (ELT Overview)


<img width="1714" height="1545" alt="image" src="https://github.com/user-attachments/assets/ea3b2a33-9a8c-4df0-85ba-be7fcaae4035" />



