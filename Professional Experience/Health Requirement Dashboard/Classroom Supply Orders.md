### Classroom Supply Orders
**Purpose:** Normalize wide classroom supply requests into a long-format fact table.

**Steps:**
1. Connect to SQL database and load `vClasroomSupplyOrders`
2. Cast item fields to text for cleaning
3. Replace "true"/"false" with 1/0 for numeric conversion
4. Convert to Int64.Type for analysis
5. Unpivot item columns into long-form records
6. Merge with `Classroom_Mapping` for item/category names
7. Merge with `Site` for site-level context
8. Filter out deleted records (`DeleteDate = null`)
9. Add source tracking and rename key fields

---

**PowerQuery Editor Code Snippet**
```m
let
    Source = Sql.Database("<SQL_SERVER>"),
    Database = Source{[Name="<DB_NAME>"]}[Data],
    RawView = Database{[Schema="<SCHEMA>", Item="<VIEW_NAME>"]}[Data],
    ChangedType = Table.TransformColumnTypes(RawView, {{"<columns>", type text}}),
    ReplacedTrue = Table.ReplaceValue(ChangedType, "true", "1", Replacer.ReplaceText, {"<columns>"}),
    ReplacedFalse = Table.ReplaceValue(ReplacedTrue, "false", "0", Replacer.ReplaceText, {"<columns>"}),
    ConvertedToInt = Table.TransformColumnTypes(ReplacedFalse, {{"<columns>", Int64.Type}}),
    Unpivoted = Table.Unpivot(ConvertedToInt, {"<columns>"}, "Item", "Quantity"),
    MergedMapping = Table.NestedJoin(Unpivoted, {"Item"}, Classroom_Mapping, {"Code"}, "Mapping", JoinKind.LeftOuter),
    ExpandedMapping = Table.ExpandTableColumn(MergedMapping, "Mapping", {"Category", "Item"}, {"Category", "Item"}),
    AddedSource = Table.AddColumn(ExpandedMapping, "Source", each "Classroom Supply Orders")
in
    AddedSource
