
# 02 — Data Lake Design (Bronze / Silver / Gold)

Este documento descreve o desenho do Data Lake em três camadas **Bronze → Silver → Gold**, as convenções de nomenclatura, os padrões de particionamento, e os recursos de
**Delta Lake** usadosp ara **Schema Evolution** e **Time Travel**. O objetivo é garantir dados auditáveis, padronizados e prontos para consumo analítico (BI/ML) com governança.

## Convenções de Nomenclaturas

**Padrões de diretórios e arquivos:**

- **Bronze (raw/ landing zone):**

bronze/<dominio>/<tabela>/ingestion_date=YYYY-MM-DD/part-*.parquet

- **Silver (curated/conformed):**

siver/<dominio>/<tabela>

Com colunas padronizadas:

- created_at (timestamp de criação no sistema de origem)
- updated_at (timestamp de útlima utilização no sistema de origem)
- ingestion_timestam (timestamp de ingestão no lake)

- **Gold (analytics / marts/):**

gold/<area_analitica>/<mart>/

Modelado de forma **dimensional** (esquema em estrela: fatos e dimensões).

**Domínio** representa um contexto de negócio (ex.: financeiro, vendas, logistica).
**Mart** representa um conjunto de tabelas analíticas de uma área (ex.: vendas_diarias, fraude, churn).

## Visão Geral do Fluxo (Bronze → Silver → Gold)

1. **Bronze**: ingestão *bruta* (sem transformação) em formato **Parquet/Delta**, com **particionamento por data de ingestão**

2. **Silver**: limpeza, padronização de tipos e colunas, enriquecimentos e aplicação de regras de negócio. Tabelas versionadas com **Delta Lake**

3. **Gold**: modelagem **dimensional** (fatos/dimensões), agragações e KPIs prontos para o consumo por **BI** ou **ML**.

________________________________________________________________________________________________________________________

## Bronze -- Raw / Landing

### Obejtivo

Preservar os dados **exatamente como vieram** da origem, com **histórico completo** e rastreabilidade.

#### O que acontece nesta etapa

- Conexão às fontes (DBs, APIs, arquivos, sistemas legados)
- Ingestão contínua ou em batch
- Escrita **imutável** no Data Lake, particionada por ingestion_date.
- Registro de metadados de ingestão (ex.: ingestion_timestamp)
- Preferência por **Delta Lake** (transações ACID + versionamento)

#### Boas práticas

- **Não transformar** o conteúdo além do necessário para armazenamento
- **Registrar a Origem** (sistema, dataset, extração)
- **Validar integridade** (linhas lidas vs. gravadas).
- **Small files**: usar Auto Loader, *trigger once* e/ou *optimize* para evitar fragmentação

________________________________________________________________________________________________________________________

## Silver — Clean / Refined / Conformed

### Objetivo

Entregar dados **limpos, padronizados e consistentes**, prontos para reuso por múltiplas áreas.

- **O que acontece nesta etapa**

#### Limpeza e Padronização

- Tipos de dados consistentes,
- remoção de duplicidades,
- tratamento de nulos e outliers,
- normalização de códigos de formatos.

#### Enriquecimento

- *joins* com tabelas de referência,
- derivação de colunas (ex.: faixas, status).

#### Regras de negócio

- validações, filtros e deduplicações determinísticas

#### Padronização de Colunas

- created_at, updated_at, ingestion_timestamp.

#### Schema Evolution e Time Travel via Delta Lake

#### Chaves técnicas quando necessário (ex.: surrogate_key)

#### Boas Práticas

- Usar *MERGE INTO* para upsets confiáveis
- Validar qualidade (contagens, business rules, expectations).
- Minimizar skew de partições (escolher bem colunas de particionamento)
- Documentar *line age* e regras aplicadas

________________________________________________________________________________________________________________________

## Gold — Analytics / Data Marts

### Objetiv0

Oferecer dados **modelados para consumo** (BI/BL), com **métricas confiáveis** e desempenho de consulta. 

- **O que acontece nesta etapa**

- **Modelagem dimensional** (estrela)
  - **Tabela Fato**: medidas (ex.: vendas, transações)
  - **Tabela Dimensão**: contexto (ex.: clientem produto, tempo)
- **Agregações e KPIs**: oficiais do negócio.
- **Otimizações** de leitura (Z-ordering, clustering, otimize, caching).
- Publicação para ferramentas de BI (Power BI, Databricks SQL).

#### Boas Práticas 

- Definir **grão** das tabelas fato de forma clara e imutável.
- Garantir **conformidade** das dimensões (dimensões compartilhadas).
- Evitar *over-aggregation;* manter fatos no graõ transacional quando fizer sentido.
- **SCDs** (Type 1/2) nas dimensões quando necessário

________________________________________________________________________________________________________________________

## Ferramentas Principais por Etapa

| Etapa      | Ferramentas / Serviços                                                                                                |
|------------|-----------------------------------------------------------------------------------------------------------------------|
| Bronze     | Databricks Auto Loader, Spark Structured Streaming/Batch, Delta Lake, Parquet, Azure Data Factory/Synapse Integration |
| Silver     | Apache Spark (PySpark/SQL), Delta Lake (MERGE, schema evolution, time travel), Databricks Workflows, Unity Catalog    |
| Gold       | Delta Lake, Databricks SQL, Power BI, Data Explorer, Z-Ordering/Optimize, Caching                                     |
| Governança | Unity Catalog (metastore, permissões, lineage), tags de dados, auditoria                                              |
