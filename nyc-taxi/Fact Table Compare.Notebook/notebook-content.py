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
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
lh_details = spark.sql("DESCRIBE DETAIL gold.fact_trips").collect()[0]

wh_details = spark.sql("DESCRIBE DETAIL 'abfss://8cdf1706-1fd1-4985-9125-a22e233cd933@onelake.dfs.fabric.microsoft.com/5bb714db-73b7-4697-a179-2e9b0d5ad4ae/Tables/gold/fact_trips'").collect()[0]

print("=== Lakehouse fact_trips ===")
print(f"Size: {lh_details['sizeInBytes'] / (1024**3):.2f} GB")
print(f"Files: {lh_details['numFiles']}")

print("\n=== Warehouse fact_trips ===")
print(f"Size: {wh_details['sizeInBytes'] / (1024**3):.2f} GB")
print(f"Files: {wh_details['numFiles']}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
