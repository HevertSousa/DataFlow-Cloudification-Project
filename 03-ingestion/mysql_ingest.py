
# Ingestão de dados MySQL para Bronze (Delta)
# Rode em Databricks (PySpark) ou local com Spark configurado.

import os, datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB   = os.getenv("MYSQL_DB", "erp")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASSWORD")
BRONZE     = os.getenv("BRONZE_PATH", "/mnt/datalake/bronze")

TABLE = os.getenv("MYSQL_TABLE", "customers")
DOMAIN = os.getenv("DOMAIN", "erp")

spark = SparkSession.builder.appName("mysql_ingest").getOrCreate()

jdbc_url = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?useSSL=false&allowPublicKeyRetrieval=true"
props = {
    "user": MYSQL_USER,
    "password": MYSQL_PASS,
    "driver": "com.mysql.cj.jdbc.Driver",
}

print(f"Lendo tabela {TABLE} do MySQL...")
df = spark.read.jdbc(url=jdbc_url, table=TABLE, properties=props)

df = df.withColumn("ingestion_timestamp", current_timestamp())

out_path = f"{BRONZE}/{DOMAIN}/{TABLE}/ingestion_date={datetime.date.today()}"
print(f"Gravando Delta em {out_path}")
df.write.format("delta").mode("append").save(out_path)

print("Ingestão concluída.")
