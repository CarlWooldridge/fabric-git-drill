-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "5838af0b-f450-4a52-8644-a7269ea77912",
-- META       "default_lakehouse_name": "NYCTaxiLH",
-- META       "default_lakehouse_workspace_id": "8cdf1706-1fd1-4985-9125-a22e233cd933",
-- META       "known_lakehouses": [
-- META         {
-- META           "id": "5838af0b-f450-4a52-8644-a7269ea77912"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- MARKDOWN ********************

-- # Create materialized lake views 
-- 1. Use this notebook to create materialized lake views. 
-- 2. Select **Run all** to run the notebook. 
-- 3. When the notebook run is completed, return to your lakehouse and refresh your materialized lake views graph. 


-- CELL ********************

-- Welcome to your new notebook 
-- Type here in the cell editor to add code! 
 CREATE MATERIALIZED LAKE VIEW dbo.taxi_summary_mlv
  AS
SELECT 
    COUNT(*) AS row_count,
    AVG(CAST(tripDistance AS FLOAT)) AS avg_distance,
    SUM(CAST(totalAmount AS FLOAT)) AS total_revenue
FROM dbo.taxi_rides_copy_activity_optimize;

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
