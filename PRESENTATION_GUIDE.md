# Guia de Apresentação: Astronomer Airflow
## Orquestrando Data Engineering e Machine Learning na Nuvem

**Duração:** 40 minutos  
**Cargo:** Data Engineer and Scientist

---

## Estrutura da Apresentação

### 1. **Introdução: O que é Astronomer Airflow?** (5 min)
- Contexto do Apache Airflow
- Como Astronomer surgiu e suas vantagens
- Por que usar Astronomer para MLOps?

**Demo:** Mostrar o Airflow UI e estrutura do projeto

### 2. **Setup e Configuração** (8 min)
- Infraestrutura (Docker, Astronomer Runtime)
- Estrutura do projeto
- DAGs, Executors, configuração
- Observabilidade (logs, métricas, UI)

**Demo:** Navegar pelo projeto, mostrar Dockerfile, estrutura de pastas

### 3. **Tutorial Básico de Airflow** (10 min)
- Criação de DAGs
- Operadores (Python, BigQuery, Dataproc)
- Dependências entre tarefas
- Dynamic Task Mapping
- Variáveis e Macros do Airflow

**Demo:** Criar um DAG simples, mostrar tasks, executar e ver logs

### 4. **Data Engineering + Machine Learning** (10 min)
- Automação de ETL
- Feature Engineering
- Training Pipeline
- Versionamento de Modelos
- Deploy e Inferência

**Demo:** Mostrar DAGs completos: ingestão, treino, inferência

### 5. **Integração com GCP** (5 min)
- BigQuery: Armazenamento e consultas
- Dataproc: Processamento paralelo (Spark)
- Vertex AI: Training e Model Registry

**Demo:** Executar pipeline que usa todas essas tecnologias

### 6. **Q&A** (2 min)

---

## Script de Demo

### Setup Inicial (Antes de Começar)

```bash
# Navegar até o diretório do projeto
cd d:\dev\data-science\airflow-mlops-template

# Build da imagem Docker
docker build -f astro/Dockerfile -t airflow-demo .
```

---

## Segmento 1: Introdução (5 min)

### Slides/Fala:
"O Apache Airflow é uma plataforma open-source para orquestração de workflows. O Astronomer, fundado pelos criadores do Airflow, oferece uma versão enterprise com recursos adicionais e melhor suporte."

### Demo:
```bash
# Mostrar estrutura do projeto
ls -la
# Mostrar:
# - astro/ (configuração do Airflow)
# - feature-code/ (código ML e SQL)
# - README.md (documentação)
```

### Mostrar na UI do Airflow:
- Visão geral dos DAGs
- Links rápidos para a documentação
- Astronomer Runtime version

---

## Segmento 2: Setup e Configuração (8 min)

### Slides/Fala:
"Vamos entender como está estruturado nosso ambiente Astronomer Airflow."

### Demo:
1. **Mostrar Dockerfile**
```dockerfile
# Destacar:
# - Base image Astronomer Runtime
# - Dependências (requirements.txt)
# - Estrutura de pastas
```

2. **Mostrar Estrutura de Pastas**
```
astro/
├── dags/              # DAGs do Airflow
├── config/            # Configurações YAML
├── dag_builder/       # Gerador de DAGs dinâmicos
├── templates/         # Templates Jinja2
└── Dockerfile         # Build da imagem

feature-code/
├── src/               # Código Python (train, predict, preprocess)
└── sql/               # Queries SQL
```

3. **Mostrar Configuração YAML (ingestion.yaml)**
```yaml
# Destacar:
# - DAG metadata (nome, schedule, tags)
# - Environment-specific configs
# - Task definitions com SQL files
```

4. **Mostrar Airflow UI**
- Acessar http://localhost:8080
- Mostrar Admin -> Variables
- Mostrar Admin -> Connections
- Mostrar DAGs na interface

---

## Segmento 3: Tutorial Básico (10 min)

### Demo 1: DAG Simples com Python Operator

**Slides/Fala:** "Vamos criar nosso primeiro DAG simples usando o TaskFlow API."

**Arquivo:** `astro/dags/demo_simple.py`

```python
from airflow.decorators import dag, task
from pendulum import datetime

@dag(
    dag_id="demo_simple",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
)
def demo_simple():
    @task
    def extract():
        return {"data": "hello from task 1"}

    @task
    def transform(data):
        return {"transformed": data["data"].upper()}

    @task
    def load(data):
        print(f"Loading: {data}")

    data = extract()
    transformed = transform(data)
    load(transformed)

demo_simple()
```

**Ação na UI:**
1. Mostrar o DAG na interface
2. Trigger o DAG manualmente
3. Mostrar execução das tasks
4. Mostrar logs de cada task
5. Mostrar XCom para ver dados compartilhados

---

### Demo 2: BigQuery Operator

**Slides/Fala:** "Agora vamos adicionar integração com BigQuery."

**Mostrar:** arquivo `astro/dags/exampledag.py` (já existe)

**Ação na UI:**
1. Mostrar o DAG `example_astronauts`
2. Mostrar código (API call, XCom, dynamic mapping)
3. Trigger e executar
4. Mostrar BigQuery Console para ver resultados

---

### Demo 3: Dependências Complexas

**Slides/Fala:** "Vamos ver dependências entre tarefas."

**Mostrar:** `astro/dags/data_ingestion_pipeline.py`

**Pontos a destacar:**
- Extracting data
- Validating data
- Loading to warehouse
- Dependencies: extract → validate → load
- Mostrar gráfico de dependências no UI

---

## Segmento 4: Data Engineering + ML (10 min)

### Demo 1: Pipeline de Ingestão de Dados

**Arquivo:** `astro/dags/data_ingestion_pipeline.py`

**Executar:**
1. Mostrar o DAG
2. Mostrar configuração YAML (`astro/config/ingestion.yaml`)
3. Mostrar SQL files (`feature-code/sql/ingestion_*.sql`)
4. Trigger o DAG
5. Destacar:
   - BigQuery queries
   - Data quality validation
   - Incremental loads (WRITE_APPEND)
   - Partitioned tables

---

### Demo 2: Pipeline de ML Training

**Arquivo:** Config `astro/config/training.yaml`

**Slides/Fala:** "Agora vamos combinar Data Engineering com ML."

**Mostrar arquivos:**
1. `training.yaml` - configuração completa
2. `feature-code/src/train/train.py` - código de treino
3. `feature-code/src/preprocess/preprocess.py` - feature engineering

**Pontos a destacar:**
- BigQuery: preparar dados de treino
- Dataproc: processar com Spark
- Feature engineering
- Model training
- Model evaluation e métricas
- Model versioning

---

### Demo 3: Pipeline de Inferência

**Arquivo:** `astro/config/model_inference.yaml`

**Mostrar:**
1. Batch inference com modelo treinado
2. Post-processing de predictions
3. Salvando predictions no BigQuery

---

## Segmento 5: Integração GCP (5 min)

### Demo: Pipeline Completo E2E

**Slides/Fala:** "Vamos executar um pipeline end-to-end que usa todas as ferramentas GCP."

**Passos:**
1. **BigQuery** - Extração e transformação de dados
2. **Dataproc** - Feature engineering distribuído
3. **Vertex AI** - Training do modelo
4. **BigQuery** - Salvando métricas
5. **Dataproc** - Batch inference
6. **BigQuery** - Predictions finais

**Mostrar na UI:**
- DAG completo com todas as integrações
- Logs de cada operador
- Status de execução
- Gráfico de dependências
- Tempo de execução

**Mostrar no Console GCP:**
- BigQuery: tabelas criadas
- Dataproc: jobs executados
- Vertex AI: modelos registrados

---

## Segmento 6: Q&A (2 min)

**Pontos para destacar se perguntarem:**

1. **Escalabilidade:** Como escalar com Kubernetes, múltiplos workers
2. **Observabilidade:** Integração com Datadog, Prometheus, Grafana
3. **CI/CD:** Deployment automatizado, testes de DAGs
4. **Custos:** Otimização de Dataproc clusters, cache do BigQuery
5. **Versionamento:** Git para código, MLflow para modelos

---

## Comandos Úteis Durante a Demo

### Iniciar Airflow Local
```bash
# Se estiver usando Astro CLI
astro dev start

# Ou com Docker
docker run -p 8080:8080 airflow-demo
```

### Ver Logs
```bash
# Terminal
docker logs <container_id>

# UI do Airflow: clicar em task → logs
```

### Executar DAGs
```bash
# CLI do Airflow
airflow dags trigger <dag_id>

# Ou pela UI: clicar em "Trigger DAG"
```

### Verificar Configurações
```bash
# Environment variables
docker exec <container> env | grep GCP

# Airflow connections
airflow connections list

# Airflow variables
airflow variables list
```

---

## Checklist Antes da Apresentação

- [ ] Docker build funcionando
- [ ] Airflow UI acessível na porta 8080
- [ ] Credenciais GCP configuradas
- [ ] DAGs aparecendo na interface
- [ ] Exemplo de DAGs rodando
- [ ] BigQuery projeto configurado
- [ ] Dataproc permissions configuradas
- [ ] Slides preparados
- [ ] Backup de screenshots da UI
- [ ] Código de exemplo funcionando

---

## Recursos Adicionais

### Links Úteis
- [Astronomer Docs](https://docs.astronomer.io/)
- [Airflow Docs](https://airflow.apache.org/)
- [GCP Integration](https://cloud.google.com/composer/docs)
- [Astronomer Academy](https://www.astronomer.io/learn/)

### Código de Referência
- `astro/dags/` - DAGs de exemplo
- `astro/config/` - Configurações
- `feature-code/src/` - Código ML
- `feature-code/sql/` - SQL queries

---

## Estrutura Recomendada para Apresentação

```
1. Introdução e Contexto           (5 min)
   ├─ Astronomer vs Apache Airflow
   ├─ Visão geral da arquitetura
   └─ Demo: UI do Airflow

2. Setup e Infraestrutura          (8 min)
   ├─ Docker e Astronomer Runtime
   ├─ Estrutura do projeto
   ├─ Configurações YAML
   └─ Demo: Navegar pelo código

3. Tutorial Básico                  (10 min)
   ├─ DAGs simples
   ├─ Operadores (Python, BigQuery)
   ├─ Dependências
   └─ Demo: Criar e executar DAG

4. Data Engineering + ML            (10 min)
   ├─ Pipeline ETL
   ├─ Training pipeline
   ├─ Inferência
   └─ Demo: Pipeline completo

5. Integração GCP                   (5 min)
   ├─ BigQuery
   ├─ Dataproc
   ├─ Vertex AI
   └─ Demo: E2E pipeline

6. Q&A                              (2 min)
   └─ Tópicos adicionais
```

---

**Boa apresentação! 🚀**

