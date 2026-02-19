
# Configura provider Databricks apontando para o workspace criado no módulo Azure
provider "databricks" {
  azure_workspace_resource_id = var.databricks_workspace_id
}

# Exemplo: criar recursos somente se habilitado
locals {
  create = var.enable_databricks_resources
}

# Cluster de engenharia simples (custo baixo). Ajuste node_type/size conforme sua região/conta.
resource "databricks_cluster" "engineers" {
  count                   = local.create ? 1 : 0
  cluster_name            = "engineers"
  spark_version           = "13.3.x-scala2.12"
  node_type_id            = "Standard_DS3_v2"
  autotermination_minutes = 30
  num_workers             = 1
}

# SQL Warehouse básico
resource "databricks_sql_endpoint" "bi_warehouse" {
  count                     = local.create ? 1 : 0
  name                      = "bi-warehouse"
  cluster_size              = "2X-Small"
  auto_stop_mins            = 30
  enable_serverless_compute = true
}
