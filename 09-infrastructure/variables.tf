
variable "project_prefix" {
  type        = string
  description = "Prefixo do projeto para nomenclatura."
  default     = "dataflow"
}

variable "env_name" {
  type        = string
  description = "Nome do ambiente (ex.: dev, prod)."
}

variable "location" {
  type        = string
  description = "Região Azure."
  default     = "brazilsouth"
}

variable "tags" {
  type        = map(string)
  description = "Tags padrão."
  default     = {
    owner   = "data-eng"
    project = "dataflow-cloudification"
  }
}

variable "enable_databricks_resources" {
  type        = bool
  description = "Se true, cria cluster/warehouse de exemplo no módulo Databricks."
  default     = true
}
