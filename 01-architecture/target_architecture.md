
# 1 — Arquitetura do Projeto 

## 1.1 - Objetivo da Arquitetura

A arquitetura deste projeto foi desenhada para demonstrar uma jornada completa de **cloudification de pipeline de dados**, cobrindo ingestão, transformação, qualidade, 
governança e disponibilização de dados em uma arquitetura moderna, escalável e resiliente. 

O propósito deste módulo é: 
- Fornecer **uma visão macro** da plataforma de dados proposta. 
- Explicar as **decisões arquiteturais** adotadas. 
- Descrever como os componentes se relacionam dentro do fluxo completo. 
- Servir como base para os demais diretórios do portfólio (infra, ingestion, governance, pipelines etc).

Diagramas e decisões de arquitetura.

## Visão Geral da arquitetura
A arquitetura segue um padrão baseado em camadas, amplamente utilizado em projetos modernos de engenharia de dados.

[Fontes] → [Ingestion] → [Bronze] → [Silver] → [Gold] → [Serviços]

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

### ADR-001 — Formato de armazenamento
**Decisão:** Usar Delta Lake.  
**Por quê:** Precisamos de ACID, time travel, merge otimizado e esquemas evolutivos.  
**Impacto:** Pipelines mais confiáveis, governança mais forte, simplicidade na manutenção.

## Camadas Principais
### Ingestion Layer 
Responsável por adquirir dados de diferentes origens: 
- Bancos Legados(MySQL, DB2)
- Arquivos estruturados e semi estruturados
- APIs internas/externas
- Streams (eventos)
Métodos de Ingestão
- Batch (incremental e full load)
- CDC(Change Data Capture), quando aplicável
- Micro-Batches

### Data Lake Zones
Para fins didáticos, seguirei as três zonas classícas: 

CAMADA                      | Finalidade
**RAW (Bronze)**            | Dados brutos, sem alterações, preservam integridade da origem
**Staged/Refined (Silver)** | Padronização, limpeza, conformidade de tipos e schema
**Curated/Semantic (Gold)** | Modelos analíticos prontos para consumo

### Transformation Layer
Nesta etapa estarão
- Regras de negócio
- Padronização de schemas
- Tratamento de tipos, anomalias e valores faltantes
- Agregações, conformidade e derivação de atributos
- Modelagem analítica (Dimensional ou Data Vault)
Ferramentas/abordagens típicas: 
- Spark / Pyspark
- dbt
- Beam
- SQL engines distribuídos

### Governance & Quality Layer
Composto por: 
- Data quality rules(completeness, validity, uniqueness...)
- Data Lineage (rastreamento de origem → destino)
- Data Contracts entre produtores e consumidores
- Metadados técnicos e de negócios 
- Monitoramento e documentação viva

### Orchestration Layer
Define dependências, agendamentos e trigger conditions. Exemplos comuns são:
- Airflow
- Databricks Workflows
- AWS Step Functions / GCP Composer / Azure Data Factory

### Serving Layer
Consumo final para: 
- Dashboards (Power BI, Looker, Tableau)
- Microserviços
- APIs
- Feature Stores
- Aplicações IA e modelos ML

## Decisões Arquiteturais
As principais decisões para este projeto incluem: 
### Cloud First Strategy
Toda a arquitetura foi desenhada para rodar nativamente em ambientes cloud, garantido: 
- Elasticidade
- Cost governance
- Security by design
- Observabilidade
### Data Lake como núcleo
Por garantir: 
- Baixo custo de armazenamento
- Escalabilidade quase ilimitada 
- Flexibilidade de formatos e estruturas
- Separação entre storage e compute
### Processamento distribuído
Utilização de sistemas escaláveis para transformação massiva de dados, garantido: 
- Performance
- Resiliência
- Paralelização automática
### Orquestração desacoplada
Separar a lógica de negócio da lógica de agendamento e dependências. 
### Modelo de Segurança Zero-Trust
Incluindo:
- Roles segregadas
- Controle de acesso por camadas 
- Encryption at rest e in transit
- Governança de metadados e owners por domínio

## Benefícios da Arquitetura
- Escalabilidade horizontal
- Redução de acoplamento entre etapas
- Observabilidade completa do pipeline
- Tratamento adequado de dados legados
- Modularidade (cada diretório do repositório mostra um pedaço isolado)
- Excelente como **portfólio profissional**

## Arquitetura Lógica em Camadas

```mermaid
flowchart LR
  subgraph Sources[Fontes de Dados]
    A1[MySQL]:::db
    A2[DB2]:::db
    A3[APIs]:::api
    A4[Arquivos]:::file
    A5[Streams]:::stream
  end

  subgraph Ingestion[Camada de Ingestão]
    B1[Batch Jobs]
    B2[CDC / Incremental]
    B3[Streaming Ingestion]
  end

  subgraph DL [Data Lake Zones]
    C1[bronze\nRaw]
    C2[Silver\nStaged]
    C3[Gold\nCurated]
  end

  subgraph Gov[Governança & Qualidade]
    E1[Data Quality Rules]
    E2[Lineage]
    E3[Data Contracts]
  end

  subgraph Serve[Camada de Consumo]
    F1[Dashboards]
    F2[APIs]
    F3[ML/Feature Store]
  end
  
  
  A1 --> B1
  A2 --> B1
  A3 --> B2
  A4 --> B1
  A5 --> B3

  B1 --> C1
  B2 --> C1
  B3 --> C1

  C1 --> C2 --> C3

  C2 --> D1
  C2 --> D2

  D1 --> C3
  D2 --> C3

  C1 --> Gov
  C2 --> Gov
  C3 --> Gov

  C3 --> Serve

  classDef db fill:#ffddcc,stroke:#b35a00,color:#000;
  classDef api fill:#ccffcc,stroke:#008000,color:#000;
  classDef file fill:#e0e0e0,stroke:#555,color:#000;
  classDef stream fill:#ccddff,stroke:#0044aa,color:#000;
```

## Pipeline end-to-end

```mermaid
sequenceDiagram
    participant FNT as Fonte de Dados
    participant ING as Ingestion Layer
    participant RAW as Raw/Bronze
    participant STG as Staged/Silver
    participant CUR as Curated/Gold
    participant GOV as Governança / DQ
    participant SRV as Serving Layer

    FNT->>ING: Envia dados (Batch/CDC/Stream)
    ING->>RAW: Grava dados brutos
    RAW->>GOV: Registro de lineage
    RAW->>STG: Limpeza e padronização

    STG->>GOV: Valida regras de qualidade
    STG->>CUR: Modelagem analítica e métricas derivadas

    CUR->>GOV: Atualiza catálogo e lineage
    CUR->>SRV: Disponibiliza datasets (BI, APIs, ML)
```
## Arquitetura Física (Genérica p/ Cloud)
```mermaid
flowchart TD
    subgraph Cloud[Ambiente Cloud]
        subgraph Network[VPC / VNets]
            LB[Load Balancer]
            API[API Gateway]
        end
        
        subgraph Storage[Storage / Data Lake]
            BRZ[Bronze Zone]
            SLV[Silver Zone]
            GLD[Gold Zone]
        end

        subgraph Compute[Compute Layer]
            SPK[Spark Cluster / Databricks]
            WF[Orquestrador<br/>Airflow / ADF / Composer]
        end

        subgraph GovSec[Governança, Segurança e Catálogo]
            CAT[Data Catalog]
            DQ[Data Quality Engine]
            MET[Metadados]
        end

        subgraph Consumption[Camada de Consumo]
            BI[Dashboards]
            API2[APIs]
            ML[Modelos ML / Feature Store]
        end
    end

    LB --> API --> SPK
    SPK --> BRZ --> SLV --> GLD
    GLD --> BI
    GLD --> API2
    GLD --> ML

    BRZ --> MET
    SLV --> MET
    GLD --> MET

    SLV --> DQ
    GLD --> DQ

    MET --> BI
```
