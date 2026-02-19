
# Move/ingere arquivos CSV de um diretório FTP/snapshot para Bronze.
# Em Databricks, prefira montar o storage/usar ADF. Aqui, exemplo simples local.

import os, shutil, datetime
from pathlib import Path

SOURCE = os.getenv("FTP_LOCAL_PATH", "data/ftp_drop/")
BRONZE = os.getenv("BRONZE_PATH", "/mnt/datalake/bronze")
DOMAIN = os.getenv("DOMAIN", "external")
TABLE  = os.getenv("FTP_TABLE", "shipments")

src = Path(SOURCE)
dst = Path(f"{BRONZE}/{DOMAIN}/{TABLE}/ingestion_date={datetime.date.today()}")

dst.mkdir(parents=True, exist_ok=True)

for f in src.glob("*.csv"):
    shutil.copy2(f, dst / f.name)
    print(f"Copiado {f} -> {dst/f.name}")

print("Arquivos movidos para Bronze. Use notebooks Spark para convertê-los em Delta.")
