
-- Exemplo: criação de tabela Gold (Databricks SQL)
CREATE TABLE IF NOT EXISTS gold.sales.fact_orders
USING DELTA
LOCATION '/mnt/datalake/gold/sales/fact_orders';
