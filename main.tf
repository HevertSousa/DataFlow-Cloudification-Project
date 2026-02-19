locals {
  rg_name        = "${var.project_prefix}-${var.env_name}-rg"
  st_name        = replace(substr("${var.project_prefix}${var.env_name}lake", 0, 24), "-", "")
  kv_name        = replace(substr("${var.project_prefix}-${var.env_name}-kv", 0, 24), "-", "")
  adf_name       = "${var.project_prefix}-${var.env_name}-adf"
  dbx_name       = "${var.project_prefix}-${var.env_name}-dbx"
}

module "azure" {
  source = "./modules/azure"

  location                  = var.location
  resource_group_name       = local.rg_name
  storage_account_name      = local.st_name
  key_vault_name            = local.kv_name
  data_factory_name         = local.adf_name
  databricks_workspace_name = local.dbx_name
  datalake_containers       = ["bronze", "silver", "gold"]
  tags                      = var.tags
}

module "databricks" {
  source = "./modules/databricks"

  databricks_workspace_id     = module.azure.databricks_workspace_id
  databricks_workspace_url    = module.azure.databricks_workspace_url
  enable_databricks_resources = var.enable_databricks_resources

  depends_on = [module.azure]
}
