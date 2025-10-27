# Demo Quick Start Guide
## Airflow MLOps Template

Este guia fornece instruções rápidas para iniciar a demonstração em 40 minutos.

---

## ⚡ Setup Rápido (5 minutos)

### 1. Pré-requisitos
```bash
# Verificar se Docker está instalado
docker --version

# Verificar se você tem acesso a GCP
gcloud auth list
```

### 2. Build da Imagem
```bash
# Navegar até o diretório raiz do projeto
cd d:\dev\data-science\airflow-mlops-template

# Build da imagem Docker
docker build -f astro/Dockerfile -t airflow-demo .
```

### 3. Configurar Variáveis de Ambiente
```bash
# Criar arquivo .env para desenvolvimento
cat > .env << 'EOF'
GCP_PROJECT_ID=seu-projeto-gcp
GCP_REGION=us-central1
GCP_BUCKET_NAME=seu-bucket-ml
GCP_SOURCE_DATASET=raw_data
GCP_TARGET_DATASET=warehouse
ENVIRONMENT=dev
EOF
```

### 4. Iniciar Airflow
```bash
# Opção 1: Com Docker Compose (recomendado)
docker-compose up -d

# Opção 2: Docker direto
docker run -d \
  --name airflow-demo \
  -p 8080:8080 \
  -e GCP_PROJECT_ID=${GCP_PROJECT_ID} \
  -e GCP_REGION=${GCP_REGION} \
  -e GCP_BUCKET_NAME=${GCP_BUCKET_NAME} \
  -e GCP_SOURCE_DATASET=${GCP_SOURCE_DATASET} \
  -e GCP_TARGET_DATASET=${GCP_TARGET_DATASET} \
  -e ENVIRONMENT=${ENVIRONMENT} \
  airflow-demo
```

### 5. Acessar Airflow UI
```
URL: http://localhost:8080
Username: airflow
Password: airflow
```

---

## 📚 Estrutura dos DAGs de Demo

### Demo 01: DAG Simples
**Arquivo:** `demo_01_simple_python.py`

**Conceitos:**
- TaskFlow API básica
- Python operators
- XCom para compartilhar dados
- Dependências simples

**Como demonstrar:**
1. Mostrar código na UI do Airflow
2. Trigger o DAG
3. Ver execution graph
4. Ver logs de cada task
5. Ver XCom values

---

### Demo 02: Dependências Complexas
**Arquivo:** `demo_02_task_dependencies.py`

**Conceitos:**
- Múltiplas dependências
- Tasks em paralelo
- Join de dependências
- Conditional logic

**Como demonstrar:**
1. Mostrar grafo de dependências
2. Trigger o DAG
3. Destacar tasks que rodam em paralelo
4. Mostrar como dependências controlam o fluxo

---

### Demo 03: BigQuery Integration
**Arquivo:** `demo_03_bigquery.py`

**Conceitos:**
- BigQueryExecuteQueryOperator
- Variáveis do Airflow
- SQL dinâmico
- Parâmetros ({{ ds }}, {{ ds_nodash }})

**Como demonstrar:**
1. Mostrar configuração de Connection
2. Mostrar uso de variáveis {{ var.value.gcp_project_id }}
3. Executar query
4. Verificar tabela no BigQuery Console

---

### Demo 04: ML Pipeline
**Arquivo:** `demo_04_ml_pipeline.py`

**Conceitos:**
- ETL pipeline
- Feature engineering
- Model training (simulado)
- Model evaluation
- Model registry

**Como demonstrar:**
1. Mostrar pipeline completo
2. Destacar cada fase (ETL → Feature → Train → Eval → Registry)
3. Executar e ver logs de cada etapa
4. Discutir integração real com Vertex AI

---

### Demo 05: Dynamic Task Mapping
**Arquivo:** `demo_05_dynamic_task_mapping.py`

**Conceitos:**
- Dynamic Task Mapping
- Expand operator
- Processar listas dinamicamente
- Tasks geradas em runtime

**Como demonstrar:**
1. Mostrar como tasks são criadas dinamicamente
2. Executar e ver múltiplas tasks sendo criadas
3. Comparar com approach tradicional

---

## 🎯 Agenda de Demonstração (40 min)

### **Parte 1: Introdução (5 min)**
- [ ] Apresentar Astronomer vs Apache Airflow
- [ ] Mostrar Airflow UI
- [ ] Navegar pelo projeto

**Arquivos a mostrar:**
- `PRESENTATION_GUIDE.md`
- Estrutura de pastas (`astro/`, `feature-code/`)

---

### **Parte 2: Setup (8 min)**
- [ ] Docker setup
- [ ] Configurações YAML
- [ ] Connections e Variables
- [ ] Observabilidade (logs, UI)

**Arquivos a mostrar:**
- `astro/Dockerfile`
- `astro/config/ingestion.yaml`
- `astro/README_DAG_BUILDER.md`

---

### **Parte 3: Tutorial Básico (10 min)**

#### Demo 1: DAG Simples (3 min)
- [ ] Mostrar `demo_01_simple_python.py`
- [ ] Explicar TaskFlow API
- [ ] Executar e ver logs

#### Demo 2: Dependências (3 min)
- [ ] Mostrar `demo_02_task_dependencies.py`
- [ ] Explicar paralelismo
- [ ] Mostrar execution graph

#### Demo 3: BigQuery (4 min)
- [ ] Mostrar `demo_03_bigquery.py`
- [ ] Executar query
- [ ] Verificar no BigQuery Console

---

### **Parte 4: Data Engineering + ML (10 min)**
- [ ] Mostrar pipeline de ingestão (`data_ingestion_pipeline.py`)
- [ ] Mostrar pipeline de ML (`demo_04_ml_pipeline.py`)
- [ ] Destacar integração ETL + ML
- [ ] Executar pipeline completo

**Arquivos a mostrar:**
- `astro/dags/data_ingestion_pipeline.py`
- `astro/dags/demo_04_ml_pipeline.py`
- `feature-code/src/train/train.py`
- `feature-code/sql/ingestion_*.sql`

---

### **Parte 5: Integração GCP (5 min)**
- [ ] Mostrar configuração de Dataproc
- [ ] Mostrar Vertex AI integration
- [ ] Executar pipeline E2E
- [ ] Mostrar resultados no GCP Console

**Arquivos a mostrar:**
- `astro/config/training.yaml`
- `astro/config/model_inference.yaml`

---

### **Parte 6: Q&A (2 min)**
- [ ] Responder perguntas
- [ ] Links úteis
- [ ] Recursos adicionais

---

## 🛠️ Comandos Úteis

### Iniciar/Parar Airflow
```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
```

### Airflow CLI
```bash
# Listar DAGs
docker exec airflow-demo airflow dags list

# Trigger DAG
docker exec airflow-demo airflow dags trigger demo_01_simple_python

# Ver logs de uma task
docker exec airflow-demo airflow tasks logs demo_01_simple_python extract_data 2024-01-01

# Ver XCom
docker exec airflow-demo airflow tasks states-for-dag-run demo_01_simple_python <run-id>
```

### Debugging
```bash
# Entrar no container
docker exec -it airflow-demo bash

# Ver variáveis de ambiente
docker exec airflow-demo env | grep GCP

# Ver connections
docker exec airflow-demo airflow connections list

# Ver variables
docker exec airflow-demo airflow variables list
```

---

## 📋 Checklist Antes da Apresentação

### Setup
- [ ] Docker build realizado com sucesso
- [ ] Airflow UI acessível em http://localhost:8080
- [ ] Credenciais GCP configuradas
- [ ] DAGs aparecendo na UI
- [ ] Connections configuradas (google_cloud_default)
- [ ] Variables configuradas (gcp_project_id, etc.)

### Testes
- [ ] Demo 01 executado com sucesso
- [ ] Demo 02 executado com sucesso
- [ ] Demo 03 conecta ao BigQuery
- [ ] Demo 04 simula pipeline ML
- [ ] Demo 05 cria tasks dinâmicas

### Preparação
- [ ] Screenshots da UI salvos
- [ ] Backup dos DAGs
- [ ] Slides preparados
- [ ] Links úteis organizados

---

## 🚨 Troubleshooting

### DAGs não aparecem na UI
```bash
# Verificar se DAGs estão na pasta correta
ls -la astro/dags/

# Verificar logs do scheduler
docker logs airflow-demo-scheduler

# Recarregar DAGs
docker exec airflow-demo airflow dags reserialize demo_01_simple_python
```

### Erro de Conexão com GCP
```bash
# Verificar credentials
gcloud auth application-default login

# Copiar credentials para container
docker cp ~/.config/gcloud airflow-demo:/home/airflow/

# Verificar connection
docker exec airflow-demo airflow connections get google_cloud_default
```

### Container não inicia
```bash
# Ver logs
docker logs airflow-demo

# Remover containers antigos
docker-compose down -v

# Rebuild sem cache
docker-compose build --no-cache
```

---

## 📊 Estrutura de Demonstração

```
Apresentação
├── 1. Introdução (5 min)
│   ├── O que é Astronomer Airflow
│   ├── Visão geral da arquitetura
│   └── Demo: UI do Airflow
│
├── 2. Setup (8 min)
│   ├── Docker e Astronomer Runtime
│   ├── Estrutura do projeto
│   ├── Configurações YAML
│   └── Observabilidade
│
├── 3. Tutorial Básico (10 min)
│   ├── DAG Simples (demo_01)
│   ├── Dependências (demo_02)
│   └── BigQuery (demo_03)
│
├── 4. Data Engineering + ML (10 min)
│   ├── Pipeline ETL
│   ├── Feature Engineering
│   ├── Training Pipeline
│   └── Inference Pipeline
│
├── 5. Integração GCP (5 min)
│   ├── BigQuery
│   ├── Dataproc
│   └── Vertex AI
│
└── 6. Q&A (2 min)
```

---

## 📚 Recursos Adicionais

### Documentação
- [Astronomer Docs](https://docs.astronomer.io/)
- [Airflow Docs](https://airflow.apache.org/)
- [GCP Integration](https://cloud.google.com/composer/docs)

### Código de Referência
- `astro/dags/` - Todos os DAGs de demo
- `astro/config/` - Configurações YAML
- `feature-code/src/` - Código ML
- `feature-code/sql/` - SQL queries

---

**Boa apresentação! 🚀**

