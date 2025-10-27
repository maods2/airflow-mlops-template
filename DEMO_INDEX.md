# Índice de Demonstração
## Astronomer Airflow MLOps Template

Este documento serve como índice central para toda a documentação e arquivos de demonstração.

---

## 📑 Documentação Principal

### Guias de Apresentação
1. **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)**  
   Guia completo para apresentação de 40 minutos
   - Script de apresentação
   - Segmentos temporais
   - Comandos para cada demo
   - Checklist pré-apresentação

2. **[DEMO_QUICK_START.md](DEMO_QUICK_START.md)**  
   Quick start para setup rápido
   - Setup em 5 minutos
   - Comandos úteis
   - Troubleshooting
   - Agenda detalhada

3. **[README.md](README.md)**  
   Overview geral do projeto
   - Descrição do projeto
   - Estrutura de arquivos
   - Arquitetura
   - Tecnologias utilizadas

---

## 🗂️ Estrutura de Arquivos

### DAGs de Demonstração
Localização: `astro/dags/`

| Arquivo | Conceitos Demonstrados | Tempo | Descrição |
|---------|----------------------|-------|-----------|
| [demo_01_simple_python.py](astro/dags/demo_01_simple_python.py) | TaskFlow API, Python Operators, XCom | 3 min | DAG simples ETL |
| [demo_02_task_dependencies.py](astro/dags/demo_02_task_dependencies.py) | Dependências, Paralelismo | 3 min | Tasks em paralelo |
| [demo_03_bigquery.py](astro/dags/demo_03_bigquery.py) | BigQuery Operator, Variáveis | 4 min | Integração BigQuery |
| [demo_04_ml_pipeline.py](astro/dags/demo_04_ml_pipeline.py) | ML Pipeline, ETL, Training | 5 min | Pipeline ML completo |
| [demo_05_dynamic_task_mapping.py](astro/dags/demo_05_dynamic_task_mapping.py) | Dynamic Mapping, Expand | 2 min | Tasks dinâmicas |
| [exampledag.py](astro/dags/exampledag.py) | XCom, Dynamic Mapping, API calls | 2 min | Exemplo Astronomer |

### DAGs de Produção
| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| [data_ingestion_pipeline.py](astro/dags/data_ingestion_pipeline.py) | BigQuery | Pipeline real de ingestão |
| [data_ingestion_pipeline_with_sql.py](astro/dags/data_ingestion_pipeline_with_sql.py) | BigQuery | Ingestão com SQL separado |
| [data_ingestion_pipeline_env_vars.py](astro/dags/data_ingestion_pipeline_env_vars.py) | BigQuery | Ingestão com env vars |

---

## 📊 Configurações YAML

Localização: `astro/config/`

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| [ingestion.yaml](astro/config/ingestion.yaml) | BigQuery | Config pipeline de ingestão |
| [training.yaml](astro/config/training.yaml) | Hybrid | Config pipeline de treino |
| [feature_engineering.yaml](astro/config/feature_engineering.yaml) | Hybrid | Config feature engineering |
| [model_inference.yaml](astro/config/model_inference.yaml) | Dataproc | Config inferência |

---

## 💻 Código ML

Localização: `feature-code/`

### Python
- `src/main.py` - Orquestrador principal
- `src/train/train.py` - Treinamento de modelos
- `src/predict/predict.py` - Predição/inferência
- `src/preprocess/preprocess.py` - Pré-processamento
- `src/test_sklearn.py` - Testes

### SQL
| Arquivo | Propósito |
|---------|-----------|
| `sql/create_raw_data_table.sql` | Cria tabela de dados brutos |
| `sql/create_warehouse_table.sql` | Cria tabela warehouse |
| `sql/create_labels_table.sql` | Cria tabela de labels |
| `sql/ingestion_extract_raw_data.sql` | Extração de dados |
| `sql/ingestion_load_to_warehouse.sql` | Load para warehouse |
| `sql/ingestion_validate_data_quality.sql` | Validação de qualidade |
| `sql/feature_engineering_*.sql` | Feature engineering |
| `sql/training_*.sql` | Preparação de dados de treino |

---

## 📚 Documentação Técnica

### Astro
- [astro/README.md](astro/README.md) - Overview do módulo
- [astro/README_DAG_BUILDER.md](astro/README_DAG_BUILDER.md) - DAG Builder
- [astro/README_ENVIRONMENT_VARIABLES.md](astro/README_ENVIRONMENT_VARIABLES.md) - Environment vars
- [astro/README_SQL_SEPARATION.md](astro/README_SQL_SEPARATION.md) - Separação SQL

### Feature Code
- [feature-code/README.md](feature-code/README.md) - Overview código ML
- [feature-code/IMPLEMENTATION_SUMMARY.md](feature-code/IMPLEMENTATION_SUMMARY.md) - Resumo implementação
- [feature-code/SKLEARN_IMPLEMENTATION.md](feature-code/SKLEARN_IMPLEMENTATION.md) - Scikit-learn

### Docker
- [README_DOCKER.md](README_DOCKER.md) - Setup Docker
- [astro/Dockerfile](astro/Dockerfile) - Dockerfile
- [build_docker.sh](build_docker.sh) - Build script Linux
- [build_docker.bat](build_docker.bat) - Build script Windows

---

## 🎯 Roteiro de Apresentação

### Segmento 1: Introdução (5 min)
**Recursos:**
- [PRESENTATION_GUIDE.md#segmento-1](PRESENTATION_GUIDE.md#segmento-1-introdução-5-min)
- Overview do projeto
- UI do Airflow

**Próximo:** Segmento 2

---

### Segmento 2: Setup (8 min)
**Recursos:**
- [astro/Dockerfile](astro/Dockerfile)
- [astro/config/ingestion.yaml](astro/config/ingestion.yaml)
- [astro/README_DAG_BUILDER.md](astro/README_DAG_BUILDER.md)
- [DEMO_QUICK_START.md#setup-rápido-5-minutos](DEMO_QUICK_START.md#-setup-rápido-5-minutos)

**Próximo:** Segmento 3

---

### Segmento 3: Tutorial Básico (10 min)
**Recursos:**
- [demo_01_simple_python.py](astro/dags/demo_01_simple_python.py) - 3 min
- [demo_02_task_dependencies.py](astro/dags/demo_02_task_dependencies.py) - 3 min
- [demo_03_bigquery.py](astro/dags/demo_03_bigquery.py) - 4 min

**Próximo:** Segmento 4

---

### Segmento 4: Data Engineering + ML (10 min)
**Recursos:**
- [data_ingestion_pipeline.py](astro/dags/data_ingestion_pipeline.py)
- [demo_04_ml_pipeline.py](astro/dags/demo_04_ml_pipeline.py)
- [feature-code/src/train/train.py](feature-code/src/train/train.py)
- [feature-code/sql/ingestion_*.sql](feature-code/sql/)

**Próximo:** Segmento 5

---

### Segmento 5: Integração GCP (5 min)
**Recursos:**
- [astro/config/training.yaml](astro/config/training.yaml)
- [astro/config/model_inference.yaml](astro/config/model_inference.yaml)
- BigQuery Console
- Dataproc Console
- Vertex AI Console

**Próximo:** Segmento 6

---

### Segmento 6: Q&A (2 min)
**Recursos:**
- [PRESENTATION_GUIDE.md#segmento-6-qa-2-min](PRESENTATION_GUIDE.md#segmento-6-qa-2-min)
- Links úteis
- Recursos adicionais

---

## 🛠️ Comandos por Segmento

### Segmento 1-2: Setup
```bash
# Build
docker build -f astro/Dockerfile -t airflow-demo .

# Run
docker run -p 8080:8080 airflow-demo

# Access
http://localhost:8080
```

### Segmento 3: DAGs Básicos
```bash
# Trigger Demo 01
docker exec airflow-demo airflow dags trigger demo_01_simple_python

# Trigger Demo 02
docker exec airflow-demo airflow dags trigger demo_02_task_dependencies

# Trigger Demo 03
docker exec airflow-demo airflow dags trigger demo_03_bigquery
```

### Segmento 4: ML Pipeline
```bash
# Trigger Ingestão
docker exec airflow-demo airflow dags trigger data_ingestion_pipeline

# Trigger ML
docker exec airflow-demo airflow dags trigger demo_04_ml_pipeline
```

### Segmento 5: GCP Integration
```bash
# Ver connections
docker exec airflow-demo airflow connections list

# Ver variables
docker exec airflow-demo airflow variables list
```

---

## 📋 Checklist por Segmento

### Antes da Apresentação
- [ ] Docker build OK
- [ ] Airflow UI acessível
- [ ] Credenciais GCP configuradas
- [ ] Todas as variáveis configuradas
- [ ] DAGs aparecem na UI
- [ ] Screenshots salvos

### Durante a Apresentação

#### Segmento 1-2: Setup
- [ ] Navegar pelo projeto
- [ ] Mostrar Dockerfile
- [ ] Mostrar YAML configs
- [ ] Mostrar UI do Airflow

#### Segmento 3: Tutorial
- [ ] Executar Demo 01
- [ ] Executar Demo 02
- [ ] Executar Demo 03
- [ ] Mostrar logs e XCom

#### Segmento 4: ML
- [ ] Executar pipeline de ingestão
- [ ] Executar pipeline de ML
- [ ] Mostrar código Python
- [ ] Mostrar SQL queries

#### Segmento 5: GCP
- [ ] Mostrar pipeline completo
- [ ] Verificar BigQuery
- [ ] Verificar Dataproc
- [ ] Verificar Vertex AI

#### Segmento 6: Q&A
- [ ] Responder perguntas
- [ ] Compartilhar links
- [ ] Fechamento

---

## 🔗 Links Úteis

### Documentação Oficial
- [Astronomer Docs](https://docs.astronomer.io/)
- [Airflow Docs](https://airflow.apache.org/)
- [GCP Integration](https://cloud.google.com/composer/docs)

### Cursos e Treinamento
- [Astronomer Academy](https://www.astronomer.io/learn/)
- [Airflow Tutorials](https://www.astronomer.io/tutorials)

### Blogs e Comunidade
- [Astronomer Blog](https://www.astronomer.io/blog/)
- [Airflow Community](https://airflow.apache.org/community/)

---

## 🎓 Próximos Passos

Após a apresentação:
1. Revisar código dos DAGs de demo
2. Explorar configurações YAML
3. Customizar para seu caso de uso
4. Implementar integrações reais
5. Deploy em produção

---

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte [DEMO_QUICK_START.md#-troubleshooting](DEMO_QUICK_START.md#-troubleshooting)
- Veja [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)
- Consulte a [documentação oficial](https://docs.astronomer.io/)

---

**Boa apresentação! 🚀**

