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

spark.read.table("gold.dim_date").limit(1000).toPandas().to_csv(
    "/lakehouse/default/Files/dim_date_sample.csv", index=False
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
