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

import pyspark.sql.functions as F

df = spark.read.table("dbo.taxi_rides_copy_activity_zorder")

min_dt, max_dt = df.agg(
    F.min("lpepPickupDatetime"),
    F.max("lpepPickupDatetime")
).first()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(min_dt)
print(max_dt)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pyspark.sql.functions import *
from pyspark.sql.types import DateType

start = min_dt.replace(hour=0, minute=0, second=0, microsecond=0)
end = max_dt.replace(hour=0, minute=0, second=0, microsecond=0)

date_list = [(start + timedelta(days=i),) for i in range((end - start).days + 1)]
df = spark.createDataFrame(date_list, ["Datetime"])
df = df.withColumn("Date", col("Datetime").cast(DateType())) \
       .withColumn("Year", year(col("Datetime"))) \
       .withColumn("Month", month(col("Datetime"))) \
       .withColumn("Quarter", quarter(col("Datetime"))) \
       .withColumn("MonthName", date_format(col("Datetime"), "MMMM")) \
       .withColumn("DayName", date_format(col("Datetime"), "EEEE"))

dfh = (
       spark.read.table("external.public_holidays")
       .filter(col("countryRegionCode") == "US")
       .select(col("date"), col("holidayName"))
       .withColumn("date", to_date(col("date")))
       .withColumnRenamed("date", "HolidayDate")
       .withColumnRenamed("holidayName", "holiday")
)

df = df.join(dfh, df.Date == dfh.HolidayDate, "left").drop("HolidayDate")

# display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(df.count())
df.printSchema()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

df.write.format("delta").mode("overwrite").saveAsTable("gold.dim_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimLocation.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_location_from")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimLocation.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_location_to")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimRateCode.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_ratecode")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimTripType.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_triptype")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimVendor.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_vendor")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").option("inferSchema", "true").load("Files/DimPaymentType.csv")
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold.dim_paymenttype")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TABLE gold.fact_trips
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT vendorID
# MAGIC       ,lpepPickupDatetime AS PickupDatetime
# MAGIC       ,lpepDropoffDatetime AS DropoffDatetime
# MAGIC       ,CAST(lpepPickupDatetime AS date) AS PickupDate
# MAGIC       ,CAST(lpepDropoffDatetime AS date) AS DropoffDate
# MAGIC       ,DATEDIFF(SECOND, lpepPickupDatetime,lpepDropoffDatetime) AS Duration
# MAGIC       ,passengerCount
# MAGIC       ,tripDistance
# MAGIC       ,CAST(puLocationId AS int) AS puLocationId
# MAGIC       ,CAST(doLocationId AS int) AS doLocationId
# MAGIC       ,pickupLongitude
# MAGIC       ,pickupLatitude
# MAGIC       ,dropoffLongitude
# MAGIC       ,dropoffLatitude
# MAGIC       ,rateCodeID
# MAGIC       ,storeAndFwdFlag
# MAGIC       ,paymentType
# MAGIC       ,fareAmount
# MAGIC       ,extra
# MAGIC       ,mtaTax
# MAGIC       ,improvementSurcharge
# MAGIC       ,tipAmount
# MAGIC       ,tollsAmount
# MAGIC       ,ehailFee
# MAGIC       ,totalAmount
# MAGIC       ,tripType
# MAGIC   FROM dbo.taxi_rides_copy_activity_zorder

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(spark.sql("DESCRIBE DETAIL gold.fact_trips").collect()[0])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

import builtins

tables_df = spark.sql("SHOW TABLES IN gold")
tables = [row.tableName for row in tables_df.collect()]

results = []
for tbl in tables:
    tbl_name = f"gold.{tbl}"
    details = spark.sql(f"DESCRIBE DETAIL {tbl_name}").collect()[0]
    results.append({
        "table": tbl,
        "size_gb": builtins.round(details["sizeInBytes"] / (1024**3), 2),
        "num_files": details["numFiles"],
        "avg_file_size_mb": builtins.round((details["sizeInBytes"] / details["numFiles"]) / (1024**2), 2)
    })

summary_df = spark.createDataFrame(results).select(
    "table", "size_gb", "num_files", "avg_file_size_mb"
)
display(summary_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

spark.sql("OPTIMIZE gold.fact_trips ZORDER BY (PickupDate) VORDER;")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

tables_df = spark.sql("SHOW TABLES IN gold")
dim_tables = [row.tableName for row in tables_df.collect() if row.tableName.startswith("dim")]

print(f"Found {len(dim_tables)} dim tables: {dim_tables}")

for tbl in dim_tables:
    full_name = f"gold.{tbl}"
    details = spark.sql(f"DESCRIBE DETAIL {full_name}").collect()[0]
    if details["numFiles"] > 1:
        print(f"Optimizing {full_name} ({details['numFiles']} files)")
        spark.sql(f"OPTIMIZE {full_name}")
    else:
        print(f"Skipping {full_name} — already 1 file, no benefit")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

tables_df = spark.sql("SHOW TABLES IN gold")
dim_tables = [row.tableName for row in tables_df.collect() if row.tableName.startswith("dim")]

print(f"Found {len(dim_tables)} dim tables: {dim_tables}")

for tbl in dim_tables:
    full_name = f"gold.{tbl}"
    details = spark.sql(f"DESCRIBE DETAIL {full_name}").collect()[0]
    print(f"Optimizing {full_name} ({details['numFiles']} files)")
    spark.sql(f"OPTIMIZE {full_name} VORDER;")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
