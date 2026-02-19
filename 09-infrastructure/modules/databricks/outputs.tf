
output "cluster_id" {
  value       = try(databricks_cluster.engineers[0].id, null)
  description = "ID do cluster criado (se habilitado)."
}

output "sql_warehouse_id" {
  value       = try(databricks_sql_endpoint.bi_warehouse[0].id, null)
  description = "ID do SQL Warehouse (se habilitado)."
}
