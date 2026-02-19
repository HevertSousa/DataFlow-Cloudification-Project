
provider "azurerm" {
  features {}
}

# Provider Databricks será configurado dentro do módulo `databricks` usando
# azure_workspace_resource_id, assim não precisamos expor host/token aqui.
