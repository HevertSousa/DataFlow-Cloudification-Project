
# 03 — Ingestion

Scripts de ingestão a partir de MySQL, DB2 e FTP para a camada Bronze (Delta).

> Em Databricks, prefira configurar credenciais via **Secrets** e drivers JDBC via **Init Scripts**/Libraries.

## Requisitos
- Drivers JDBC: `com.mysql.cj.jdbc.Driver` e `com.ibm.db2.jcc.DB2Driver`.
- Variáveis de ambiente (ou Secrets) conforme `.env.example`.
