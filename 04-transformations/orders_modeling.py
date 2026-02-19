
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum
import os

spark = SparkSession.builder.appName("orders_modeling").getOrCreate()

SILVER = os.getenv("SILVER_PATH", "/mnt/datalake/silver")
GOLD   = os.getenv("GOLD_PATH", "/mnt/datalake/gold")

domain = os.getenv("DOMAIN", "erp")

orders = spark.read.format("delta").load(f"{SILVER}/{domain}/orders")
customers = spark.read.format("delta").load(f"{SILVER}/{domain}/customers")

fact_orders = (
    orders.alias("o")
    .join(customers.alias("c"), col("o.customer_id") == col("c.customer_id"), "left")
    .select(
        col("o.order_id"), col("o.order_date"), col("o.total_amount"),
        col("o.customer_id"), col("c.name").alias("customer_name"),
    )
)

fact_orders.write.format("delta").mode("overwrite").save(f"{GOLD}/sales/fact_orders")

agg_daily = (
    fact_orders
    .groupBy("order_date")
    .agg(_sum("total_amount").alias("daily_revenue"))
)
agg_daily.write.format("delta").mode("overwrite").save(f"{GOLD}/sales/agg_daily_revenue")

print("Gold atualizado: fact_orders e agg_daily_revenue.")
