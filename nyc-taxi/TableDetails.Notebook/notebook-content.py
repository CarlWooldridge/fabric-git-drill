# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5838af0b-f450-4a52-8644-a7269ea77912",
# META       "default_lakehouse_name": "NYCTaxiLH",
# META       "default_lakehouse_workspace_id": "8cdf1706-1fd1-4985-9125-a22e233cd933",
# META       "known_lakehouses": [
# META         {
# META           "id": "5838af0b-f450-4a52-8644-a7269ea77912"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

tables = ["taxi_rides_notebook", "taxi_rides_dataflow", "taxi_rides_copy_activity", "taxi_rides_copy_activity_optimize", "taxi_rides_copy_activity_vorder", "taxi_rides_copy_activity_zorder"]

results = []
for t in tables:
    details = spark.sql(f"DESCRIBE DETAIL dbo.{t}").collect()[0]
    results.append({
        "table": t,
        "size_gb": round(details["sizeInBytes"] / (1024**3), 2),
        "num_files": details["numFiles"],
        "avg_file_size_mb": round((details["sizeInBytes"] / details["numFiles"]) / (1024**2), 2)
    })

summary_df = spark.createDataFrame(results).select(
    "table", "size_gb", "num_files", "avg_file_size_mb"
)
display(summary_df)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
from delta.tables import DeltaTable

# Get table details
details = spark.sql("DESCRIBE DETAIL dbo.taxi_rides_copy_activity").collect()[0]
print(f"Table size: {details['sizeInBytes'] / (1024**3):.2f} GB")
print(f"Number of files: {details['numFiles']}")

# Average file size
avg_file_size_mb = (details['sizeInBytes'] / details['numFiles']) / (1024**2)
print(f"Average file size: {avg_file_size_mb:.2f} MB")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC DESCRIBE HISTORY dbo.taxi_rides_copy_activity


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM dbo.taxi_rides_copy_activity VERSION AS OF 3
# MAGIC --SELECT * FROM dbo.taxi_rides_copy_activity TIMESTAMP AS OF '2026-07-31'


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

tables = ["taxi_rides_notebook", "taxi_rides_dataflow", "taxi_rides_copy_activity", "taxi_rides_copy_activity_optimize", "taxi_rides_copy_activity_vorder", "taxi_rides_copy_activity_zorder"]

results = []
for t in tables:
    details = spark.sql(f"DESCRIBE DETAIL dbo.{t}").collect()[0]
    results.append({
        "table": t,
        "size_gb": round(details["sizeInBytes"] / (1024**3), 2),
        "num_files": details["numFiles"],
        "avg_file_size_mb": round((details["sizeInBytes"] / details["numFiles"]) / (1024**2), 2),
        "clustering_columns": str(details["clusteringColumns"])
    })

summary_df = spark.createDataFrame(results).select(
    "table", "size_gb", "num_files", "avg_file_size_mb", "clustering_columns"
)
display(summary_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
