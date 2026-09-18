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

from decimal import Decimal
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType

schema = StructType([
    StructField("emp_id",    IntegerType(),      False),
    StructField("emp_name",  StringType(),       False),
    StructField("region",    StringType(),       False),
    StructField("email",     StringType(),       False),
    StructField("salary",    DecimalType(10, 2), False),
    StructField("owner_upn", StringType(),       False),
])

rows = [
    (1, "Ana",  "North", "ana@contoso.com",  Decimal("82000.00"),  "ana@contoso.com"),
    (2, "Ben",  "North", "ben@contoso.com",  Decimal("91000.00"),  "ben@contoso.com"),
    (3, "Cara", "South", "cara@contoso.com", Decimal("77000.00"),  "cara@contoso.com"),
    (4, "Dev",  "South", "dev@contoso.com",  Decimal("105000.00"), "dev@contoso.com"),
    (5, "Eli",  "West",  "eli@contoso.com",  Decimal("68000.00"),  "eli@contoso.com"),
]

spark.createDataFrame(rows, schema).write.mode("overwrite").format("delta").saveAsTable("dbo.emp_demo")

spark.sql("""
    SELECT region, COUNT(*) AS n, SUM(salary) AS total
    FROM dbo.emp_demo GROUP BY region ORDER BY region
""").show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
