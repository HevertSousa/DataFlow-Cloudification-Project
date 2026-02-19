variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "storage_account_name" { type = string }
variable "key_vault_name" { type = string }
variable "data_factory_name" { type = string }
variable "databricks_workspace_name" { type = string }
variable "datalake_containers" { type = list(string) }
variable "tags" { type = map(string) }
