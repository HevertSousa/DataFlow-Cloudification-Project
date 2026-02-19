
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.lake.name
}

output "databricks_workspace_id" {
  value = azurerm_databricks_workspace.dbx.id
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.dbx.workspace_url
}
