# Astronomer Airflow MLOps Template
## Orquestrando Data Engineering e Machine Learning na Nuvem

Este repositório demonstra como usar **Astronomer Airflow** para criar pipelines de dados e machine learning orquestrados, integrando com serviços da **Google Cloud Platform (GCP)**.

---

## 📋 Sobre Esta Apresentação

**Cargo:** Data Engineer and Scientist  
**Título:** Astronomer Airflow: Orquestrando Data Engineering e Machine Learning na Nuvem  
**Duração:** 40 minutos

### Objetivos
1. Apresentar o Astronomer Airflow e suas vantagens
2. Demonstrar setup e configuração de pipelines
3. Mostrar tutorial básico de Airflow (DAGs, Operadores, Dependências)
4. Implementar soluções que unem Data Engineering e Machine Learning
5. Integrar com serviços GCP (BigQuery, Dataproc, Vertex AI)

---

## 🚀 Quick Start

### 1. Setup Rápido

```bash
# Build da imagem Docker
docker build -f astro/Dockerfile -t airflow-demo .

# Configurar variáveis de ambiente
export GCP_PROJECT_ID="seu-projeto-gcp"
export GCP_REGION="us-central1"
export GCP_BUCKET_NAME="seu-bucket-ml"

# Iniciar Airflow
docker run -p 8080:8080 \
  -e GCP_PROJECT_ID=${GCP_PROJECT_ID} \
  -e GCP_REGION=${GCP_REGION} \
  -e GCP_BUCKET_NAME=${GCP_BUCKET_NAME} \
  airflow-demo
```

### 2. Acessar Airflow UI
```
URL: http://localhost:8080
Username: airflow
Password: airflow
```

Para detalhes completos, veja [DEMO_QUICK_START.md](DEMO_QUICK_START.md)

---

## 📁 Estrutura do Repositório

```
airflow-mlops-template/
├── astro/                        # Configuração do Astronomer Airflow
│   ├── dags/                     # DAGs do Airflow
│   │   ├── demo_01_simple_python.py       # Demo 1: DAG Simples
│   │   ├── demo_02_task_dependencies.py   # Demo 2: Dependências
│   │   ├── demo_03_bigquery.py           # Demo 3: BigQuery
│   │   ├── demo_04_ml_pipeline.py        # Demo 4: ML Pipeline
│   │   ├── demo_05_dynamic_task_mapping.py # Demo 5: Dynamic Tasks
│   │   └── data_ingestion_pipeline.py    # Pipeline real de ingestão
│   ├── config/                   # Configurações YAML
│   │   ├── ingestion.yaml                # Config de ingestão
│   │   ├── training.yaml                 # Config de treino
│   │   ├── feature_engineering.yaml      # Config de features
│   │   └── model_inference.yaml         # Config de inferência
│   ├── dag_builder/              # Gerador dinâmico de DAGs
│   ├── templates/                # Templates Jinja2
│   └── Dockerfile                # Build da imagem
│
├── feature-code/                 # Código de Machine Learning
│   ├── src/                      # Código Python
│   │   ├── main.py               # Orquestrador
│   │   ├── train/                # Treinamento
│   │   ├── predict/              # Predição
│   │   └── preprocess/           # Pré-processamento
│   └── sql/                      # Queries SQL
│       ├── ingestion_*.sql       # Queries de ingestão
│       ├── training_*.sql        # Queries de treino
│       └── feature_engineering_*.sql # Queries de features
│
├── PRESENTATION_GUIDE.md         # Guia completo da apresentação
├── DEMO_QUICK_START.md           # Quick start para demo
└── README.md                     # Este arquivo
```

---

## 🎓 DAGs de Demonstração

### Demo 01: DAG Simples
**Arquivo:** `astro/dags/demo_01_simple_python.py`

Demonstra:
- TaskFlow API
- Python Operators básicos
- XCom para compartilhar dados
- Dependências simples (extract → transform → load)

### Demo 02: Dependências Complexas
**Arquivo:** `astro/dags/demo_02_task_dependencies.py`

Demonstra:
- Múltiplas dependências
- Tasks em paralelo
- Join de dependências
- Conditional branches

### Demo 03: Integração com BigQuery
**Arquivo:** `astro/dags/demo_03_bigquery.py`

Demonstra:
- BigQueryExecuteQueryOperator
- Variáveis do Airflow ({{ var.value.gcp_project_id }})
- Macros temporais ({{ ds }}, {{ ds_nodash }})
- Execução de queries SQL

### Demo 04: Pipeline de ML End-to-End
**Arquivo:** `astro/dags/demo_04_ml_pipeline.py`

Demonstra:
- ETL pipeline completo
- Feature Engineering
- Model Training (simulado)
- Model Evaluation
- Model Registry

### Demo 05: Dynamic Task Mapping
**Arquivo:** `astro/dags/demo_05_dynamic_task_mapping.py`

Demonstra:
- Dynamic Task Mapping (Airflow 2.3+)
- Expand operator
- Tasks criadas dinamicamente
- Processar listas de itens

---

## 🏗️ Arquitetura

### Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    Astronomer Airflow                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   DAGs       │  │  Operators   │  │  Scheduler  │      │
│  │              │  │              │  │             │      │
│  │ • Ingestão   │  │ • Python     │  │ • Executa   │      │
│  │ • Training   │  │ • BigQuery   │  │   tarefas   │      │
│  │ • Inference  │  │ • Dataproc   │  │ • Monitoring│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                        │
                        ├──────────────────┬─────────────────┐
                        ▼                  ▼                 ▼
                  ┌──────────┐      ┌──────────┐     ┌──────────┐
                  │BigQuery  │      │ Dataproc │     │Vertex AI │
                  │          │      │          │     │          │
                  │• Storage │      │• Spark   │     │• Training│
                  │• Queries │      │• PySpark │     │• Registry│
                  └──────────┘      └──────────┘     └──────────┘
```

### Fluxo de Dados

1. **Ingestão** → BigQuery
   - Extração de dados
   - Validação de qualidade
   - Load para warehouse

2. **Feature Engineering** → BigQuery + Dataproc
   - Preparação de dados no BigQuery
   - Processamento distribuído no Dataproc
   - Features criadas

3. **Training** → Vertex AI
   - Treinamento do modelo
   - Avaliação e métricas
   - Registry do modelo

4. **Inference** → Batch Prediction
   - Carga do modelo
   - Predições em lote
   - Salvamento de resultados

---

## 🛠️ Features Implementadas

### Data Engineering
- ✅ ETL pipeline automatizado
- ✅ Data quality validation
- ✅ Incremental data loading
- ✅ SQL queries parametrizadas
- ✅ Table partitioning e clustering

### Machine Learning
- ✅ Feature engineering pipeline
- ✅ Model training workflow
- ✅ Model evaluation e métricas
- ✅ Model versioning
- ✅ Batch inference pipeline

### Observabilidade
- ✅ Logging estruturado
- ✅ Task retries e alertas
- ✅ Email notifications
- ✅ Airflow UI para monitoring

### Integração GCP
- ✅ BigQuery para storage e queries
- ✅ Dataproc para processamento Spark
- ✅ Vertex AI para training e registry
- ✅ GCS para artifacts

---

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) | Guia completo de 40 minutos para apresentação |
| [DEMO_QUICK_START.md](DEMO_QUICK_START.md) | Quick start para setup e execução |
| [astro/README.md](astro/README.md) | Documentação do módulo Airflow |
| [astro/README_DAG_BUILDER.md](astro/README_DAG_BUILDER.md) | DAG Builder e templates |
| [astro/README_ENVIRONMENT_VARIABLES.md](astro/README_ENVIRONMENT_VARIABLES.md) | Variáveis de ambiente |
| [astro/README_SQL_SEPARATION.md](astro/README_SQL_SEPARATION.md) | Separação SQL/YAML |
| [feature-code/README.md](feature-code/README.md) | Código ML e SQL |
| [feature-code/IMPLEMENTATION_SUMMARY.md](feature-code/IMPLEMENTATION_SUMMARY.md) | Resumo da implementação |

---

## 🎯 Agenda da Apresentação

### 1. Introdução (5 min)
- O que é Astronomer Airflow?
- Contexto e história
- Por que usar Astronomer?

### 2. Setup e Configuração (8 min)
- Infraestrutura (Docker, Astronomer Runtime)
- Estrutura do projeto
- DAGs, Executors, Observabilidade

### 3. Tutorial Básico (10 min)
- Criação de DAGs
- Operadores (Python, BigQuery)
- Dependências entre tarefas
- Dynamic Task Mapping

### 4. Data Engineering + ML (10 min)
- Automação de ETL
- Feature Engineering
- Training Pipeline
- Versionamento e Deploy

### 5. Integração GCP (5 min)
- BigQuery: Storage e Queries
- Dataproc: Processamento paralelo
- Vertex AI: Training e Registry

### 6. Q&A (2 min)
- Perguntas e respostas
- Recursos adicionais

---

## 🔧 Tecnologias Utilizadas

- **Astronomer Airflow** - Orquestração
- **Apache Airflow** - Base open-source
- **Google BigQuery** - Data warehouse
- **Dataproc** - Spark processing
- **Vertex AI** - ML training e registry
- **Python** - Código ML e pipelines
- **SQL** - Queries de transformação
- **Docker** - Containerização

---

## 📖 Como Usar

### Para Apresentação
1. Siga o [DEMO_QUICK_START.md](DEMO_QUICK_START.md)
2. Consulte [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)
3. Execute os DAGs de demo em ordem

### Para Desenvolvimento
1. Configure credenciais GCP
2. Ajuste variáveis de ambiente
3. Customize configurações YAML
4. Gere novos DAGs

---

## 🤝 Contribuindo

Este repositório foi criado para demonstração. Sinta-se livre para:
- Adaptar para suas necessidades
- Adicionar novos exemplos
- Melhorar a documentação
- Sugerir melhorias

---

## 📄 Licença

Este projeto é de uso educacional e demonstrativo.

---

## 🎓 Recursos Adicionais

- [Documentação do Astronomer](https://docs.astronomer.io/)
- [Documentação do Airflow](https://airflow.apache.org/)
- [Airflow Academy](https://www.astronomer.io/learn/)
- [GCP Integration Docs](https://cloud.google.com/composer/docs)
- [Astronomer Blogs](https://www.astronomer.io/blog/)

---

**Desenvolvido para demonstração de Astronomer Airflow em ambiente de produção** 🚀

