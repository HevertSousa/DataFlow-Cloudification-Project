
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, trim, current_timestamp
import os

spark = SparkSession.builder.appName("customers_cleaning").getOrCreate()

BRONZE = os.getenv("BRONZE_PATH", "/mnt/datalake/bronze")
SILVER = os.getenv("SILVER_PATH", "/mnt/datalake/silver")

domain = os.getenv("DOMAIN", "erp")
bronze_path = f"{BRONZE}/{domain}/customers"
silver_path = f"{SILVER}/{domain}/customers"

raw = spark.read.format("delta").load(bronze_path)

clean = (
    raw
    .withColumn("name", trim(col("name")))
    .withColumn("created_at", to_timestamp("created_at"))
    .dropDuplicates(["customer_id"])
    .withColumn("last_update_ts", current_timestamp())
)

clean.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(silver_path)
print("Customers -> Silver atualizado.")
