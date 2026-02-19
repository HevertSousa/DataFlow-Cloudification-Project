
# 01 — Arquitetura

Diagramas e decisões de arquitetura.

## Diagrama Lógico
```mermaid
flowchart TB
  subgraph Ingestion[Ingestion]
    MySQL --> ADF
    DB2 --> ADF
    FTP --> ADF
  end

  ADF --> ADLS[(Data Lake - Bronze)]
  ADLS --> DBX[Databricks - Silver/Gold]
  DBX --> PBI[Power BI]
  DBX --> UC[Unity Catalog]
```

## Decisões (ADR)
- **Formato de armazenamento**: Delta Lake para ACID + time travel.
- **Orquestração**: ADF para conectividade híbrida e/ou DBX Workflows.
- **Dados sensíveis**: Segredos via Databricks Secrets/Key Vault.
