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

wh_path = "abfss://8cdf1706-1fd1-4985-9125-a22e233cd933@onelake.dfs.fabric.microsoft.com/5bb714db-73b7-4697-a179-2e9b0d5ad4ae/Tables/dbo/fact_trips"

spark.sql(f"OPTIMIZE delta.`{wh_path}` ZORDER BY (PickupDate) VORDER")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
