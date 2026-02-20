
# 02 — Data Lake Design (Bronze / Silver / Gold)

## Convenções de Nomenclatura

- `bronze/<dominio>/<tabela>/ingestion_date=YYYY-MM-DD/part-*.parquet`
- `silver/<dominio>/<tabela>/` com colunas padronizadas (`created_at`, `updated_at`, `ingestion_timestamp`).
- `gold/<area_analitica>/<mart>/` em modelo dimensional (estrela).

## Tópicos

- **Particionamento** por datas ou chaves de alto cardinalidade.
- **Schema Evolution** com Delta Lake.
- **Time Travel** para auditoria e recuperação.
