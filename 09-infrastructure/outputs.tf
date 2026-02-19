
output "resource_group_name" {
  value = module.azure.resource_group_name
}

output "storage_account_name" {
  value = module.azure.storage_account_name
}

output "databricks_workspace_id" {
  value = module.azure.databricks_workspace_id
}

output "databricks_workspace_url" {
  value = module.azure.databricks_workspace_url
}
