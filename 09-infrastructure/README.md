
# 09 — Infrastructure as Code (Terraform)

Infraestrutura do projeto provisionada com **Terraform**: Azure + Databricks + Data Lake + ADF + Key Vault.

## Pré-requisitos
- **Terraform 1.6+**
- **Azure CLI** autenticado (`az login`)
- Permissões na assinatura Azure para criar RG, Storage, KV, ADF e Databricks

> Autenticação: o provider `azurerm` usa a sessão do Azure CLI por padrão. O provider `databricks` é configurado via `azure_workspace_resource_id`, usando sua identidade do Azure (sem precisar de PAT).

## Estrutura
```
09-infrastructure/
├── backend.tf                 # (Opcional) backend remoto em Azure Storage (comentado)
├── providers.tf               # providers azurerm e databricks
├── versions.tf                # versões mínimas
├── variables.tf               # variáveis de root
├── main.tf                    # orquestra módulos
├── outputs.tf                 # saídas úteis
├── env/
│   ├── dev.tfvars            # var-file ambiente dev
│   └── prod.tfvars           # var-file ambiente prod
└── modules/
    ├── azure/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── databricks/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Como usar (DEV)
```bash
cd 09-infrastructure
az login
az account set --subscription "<SUBSCRIPTION_ID>"

terraform init
terraform plan  -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```

## Backend remoto (state) — opcional
Edite `backend.tf` e crie previamente um Storage Account/Container para `tfstate`. Depois rode:
```bash
terraform init -migrate-state
```

## Dica
- O módulo `azure` cria: Resource Group, ADLS Gen2 (containers bronze/silver/gold), Key Vault,
  Data Factory e **Azure Databricks Workspace**.
- O módulo `databricks` conecta no workspace criado e (opcionalmente) cria recursos internos
  como um **cluster de engenharia** e um **SQL Warehouse** simples.

> Desative recursos Databricks se não tiver permissões suficientes definindo `enable_databricks_resources = false` no `*.tfvars`.
