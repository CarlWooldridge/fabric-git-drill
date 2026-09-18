[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Query_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "vendorID", DestinationColumnName = "vendorID"], [SourceColumnName = "lpepPickupDatetime", DestinationColumnName = "lpepPickupDatetime"], [SourceColumnName = "lpepDropoffDatetime", DestinationColumnName = "lpepDropoffDatetime"], [SourceColumnName = "passengerCount", DestinationColumnName = "passengerCount"], [SourceColumnName = "tripDistance", DestinationColumnName = "tripDistance"], [SourceColumnName = "puLocationId", DestinationColumnName = "puLocationId"], [SourceColumnName = "doLocationId", DestinationColumnName = "doLocationId"], [SourceColumnName = "pickupLongitude", DestinationColumnName = "pickupLongitude"], [SourceColumnName = "pickupLatitude", DestinationColumnName = "pickupLatitude"], [SourceColumnName = "dropoffLongitude", DestinationColumnName = "dropoffLongitude"], [SourceColumnName = "dropoffLatitude", DestinationColumnName = "dropoffLatitude"], [SourceColumnName = "rateCodeID", DestinationColumnName = "rateCodeID"], [SourceColumnName = "storeAndFwdFlag", DestinationColumnName = "storeAndFwdFlag"], [SourceColumnName = "paymentType", DestinationColumnName = "paymentType"], [SourceColumnName = "fareAmount", DestinationColumnName = "fareAmount"], [SourceColumnName = "extra", DestinationColumnName = "extra"], [SourceColumnName = "mtaTax", DestinationColumnName = "mtaTax"], [SourceColumnName = "improvementSurcharge", DestinationColumnName = "improvementSurcharge"], [SourceColumnName = "tipAmount", DestinationColumnName = "tipAmount"], [SourceColumnName = "tollsAmount", DestinationColumnName = "tollsAmount"], [SourceColumnName = "ehailFee", DestinationColumnName = "ehailFee"], [SourceColumnName = "totalAmount", DestinationColumnName = "totalAmount"], [SourceColumnName = "tripType", DestinationColumnName = "tripType"]}], DynamicSchema = true, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared Query = let
  Source = AzureStorage.Blobs("https://azureopendatastorage.blob.core.windows.net/nyctlc"),
  #"Filtered rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "green/puYear")),
  #"Filtered rows 1" = Table.SelectRows(#"Filtered rows", each ([Extension] = ".parquet")),
  #"Filtered hidden files" = Table.SelectRows(#"Filtered rows 1", each [Attributes]?[Hidden]? <> true),
  #"Added custom" = let
    rootPath = Text.TrimEnd(Value.Metadata(Value.Type(#"Filtered hidden files"))[FileSystemTable.RootPath]?, "/"),
    combinePaths = (path1, path2) => Text.Combine({Text.TrimEnd(path1, "/"), path2}, "/"),
    getRelativePath = (path, relativeTo) => Text.Middle(path, Text.Length(relativeTo) + 1)
in
    Table.AddColumn(#"Filtered hidden files", "Relative Path", each getRelativePath(combinePaths([Folder Path], [Name]), rootPath), type text),
  #"Invoke custom function" = Table.AddColumn(#"Added custom", "Transform file", each #"Transform file"([Content])),
  #"Renamed columns" = Table.RenameColumns(#"Invoke custom function", {{"Relative Path", "Source.Name"}}),
  #"Removed other columns" = Table.SelectColumns(#"Renamed columns", {"Source.Name", "Transform file"}),
  #"Expanded table column" = Table.ExpandTableColumn(#"Removed other columns", "Transform file", Table.ColumnNames(#"Transform file"(#"Sample file"))),
  #"Changed column type" = Table.TransformColumnTypes(#"Expanded table column", {{"vendorID", Int64.Type}, {"lpepPickupDatetime", type datetime}, {"lpepDropoffDatetime", type datetime}, {"passengerCount", Int64.Type}, {"tripDistance", type number}, {"puLocationId", Int64.Type}, {"doLocationId", Int64.Type}, {"rateCodeID", Int64.Type}, {"storeAndFwdFlag", type text}, {"paymentType", Int64.Type}, {"fareAmount", type number}, {"extra", type number}, {"mtaTax", type number}, {"improvementSurcharge", type number}, {"tipAmount", type number}, {"tollsAmount", type number}, {"totalAmount", type number}, {"tripType", Int64.Type}}),
  #"Removed columns" = Table.RemoveColumns(#"Changed column type", {"Source.Name"}),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Removed columns", {{"pickupLongitude", type number}, {"pickupLatitude", type number}, {"dropoffLongitude", type number}, {"dropoffLatitude", type number}, {"ehailFee", type number}})
in
  #"Changed column type 1";
shared #"Sample file" = let
  Source = AzureStorage.Blobs("https://azureopendatastorage.blob.core.windows.net/nyctlc"),
  #"Filtered rows" = Table.SelectRows(Source, each Text.StartsWith([Name], "green/puYear")),
  #"Filtered rows 1" = Table.SelectRows(#"Filtered rows", each [Extension] = ".parquet"),
  #"Filtered hidden files" = Table.SelectRows(#"Filtered rows 1", each [Attributes]?[Hidden]? <> true),
  Navigation = #"Filtered hidden files"{0}[Content]
in
  Navigation;
shared Parameter = let
  Parameter = #"Sample file" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type binary, BinaryIdentifier = #"Sample file"]
in
  Parameter;
shared #"Transform Sample file" = let
  Source = Parquet.Document(Parameter)
in
  Source;
[FunctionQueryBinding = "{""exemplarFormulaName"":""Transform Sample file""}"]
shared #"Transform file" = (Parameter as binary) => let
  Source = Parquet.Document(Parameter)
in
  Source;
shared Query_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true]),
  Navigation_1 = Pattern{[workspaceId = "8cdf1706-1fd1-4985-9125-a22e233cd933"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "5838af0b-f450-4a52-8644-a7269ea77912"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "taxi_rides_dataflow", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
