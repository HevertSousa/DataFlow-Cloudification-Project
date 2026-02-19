
# Ingestão de dados DB2 para Bronze (Delta)
# Rode em Databricks (PySpark) com driver IBM DB2.

import os, datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

DB2_HOST = os.getenv("DB2_HOST")
DB2_PORT = os.getenv("DB2_PORT", "50000")
DB2_DB   = os.getenv("DB2_DB", "finance")
DB2_USER = os.getenv("DB2_USER")
DB2_PASS = os.getenv("DB2_PASSWORD")
BRONZE   = os.getenv("BRONZE_PATH", "/mnt/datalake/bronze")

TABLE  = os.getenv("DB2_TABLE", "ledger")
DOMAIN = os.getenv("DOMAIN", "finance")

spark = SparkSession.builder.appName("db2_ingest").getOrCreate()

jdbc_url = f"jdbc:db2://{DB2_HOST}:{DB2_PORT}/{DB2_DB}"
props = {
    "user": DB2_USER,
    "password": DB2_PASS,
    "driver": "com.ibm.db2.jcc.DB2Driver",
}

print(f"Lendo tabela {TABLE} do DB2...")
df = spark.read.jdbc(url=jdbc_url, table=TABLE, properties=props)

df = df.withColumn("ingestion_timestamp", current_timestamp())

out_path = f"{BRONZE}/{DOMAIN}/{TABLE}/ingestion_date={datetime.date.today()}"
print(f"Gravando Delta em {out_path}")
df.write.format("delta").mode("append").save(out_path)

print("Ingestão concluída.")
