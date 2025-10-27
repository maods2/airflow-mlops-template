# Fluxo Visual da Apresentação
## Astronomer Airflow: Orquestrando Data Engineering e ML na Nuvem

Este documento apresenta o fluxo visual da apresentação de 40 minutos.

---

## 📊 Visão Geral

```
╔══════════════════════════════════════════════════════════════╗
║                    APRESENTAÇÃO DE 40 MIN                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     ║
║  │ Introdução  │───▶│    Setup    │───▶│   Tutorial  │     ║
║  │  (5 min)    │    │   (8 min)   │    │  (10 min)   │     ║
║  └─────────────┘    └─────────────┘    └─────────────┘     ║
║         │                   │                   │           ║
║         │                   │                   ▼           ║
║         │                   │          ┌────────────────┐    ║
║         │                   │          │    DAGs        │    ║
║         │                   │          │  Demo 01-05    │    ║
║         │                   │          └────────────────┘    ║
║         │                   ▼                   │           ║
║         │          ┌────────────────┐           │           ║
║         │          │ Configurações   │           │           ║
║         │          │ YAML & Docker   │           │           ║
║         │          └────────────────┘           │           ║
║         ▼                   ▼                   ▼           ║
║  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ║
║  │ Data Eng +  │───▶│  Integração  │───▶│    Q&A      │    ║
║  │     ML      │    │     GCP      │    │   (2 min)   │    ║
║  │  (10 min)   │    │   (5 min)    │    │             │    ║
║  └─────────────┘    └─────────────┘    └─────────────┘    ║
║         │                   │                               ║
║         ▼                   ▼                               ║
║  ┌────────────────────────────────────────────┐            ║
║  │     BigQuery │ Dataproc │ Vertex AI       │            ║
║  └────────────────────────────────────────────┘            ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎯 Segmento 1: Introdução (5 min)

### Fluxo Visual

```
┌─────────────────────────────────────────────────────┐
│  O que é Astronomer Airflow?                       │
│  ┌───────────────────────────────────────────────┐ │
│  │ - Contexto do Apache Airflow                  │ │
│  │ - Como Astronomer surgiu                      │ │
│  │ - Vantagens do Astronomer                     │ │
│  │ - Por que usar para MLOps?                   │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Airflow UI - Overview                              │
│  ┌──────────────┐  ┌──────────────┐               │
│  │    DAGs      │  │   Stats      │               │
│  │              │  │              │               │
│  │ • demo_01    │  │ • Running    │               │
│  │ • demo_02    │  │ • Success    │               │
│  │ • demo_03    │  │ • Failed     │               │
│  └──────────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────┘
```

**Ação:** Navegar pela UI do Airflow, mostrar estrutura do projeto

---

## 🎯 Segmento 2: Setup e Configuração (8 min)

### Fluxo Visual

```
┌─────────────────────────────────────────────────────┐
│  Docker Setup                                       │
│  ┌───────────────────────────────────────────────┐ │
│  │ FROM quay.io/astronomer/astro-runtime:3.1-2  │ │
│  │ COPY requirements.txt                         │ │
│  │ RUN pip install -r requirements.txt           │ │
│  │ COPY astro/ dags/                            │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Estrutura do Projeto                               │
│  ┌──────────────────────┐  ┌────────────────────┐ │
│  │   astro/             │  │  feature-code/     │ │
│  │   ├─ dags/          │  │  ├─ src/           │ │
│  │   ├─ config/        │  │  ├─ sql/           │ │
│  │   ├─ templates/     │  │  └─ requirements.txt│ │
│  │   └─ Dockerfile     │  │                     │ │
│  └──────────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Configurações YAML                                │
│  ┌───────────────────────────────────────────────┐ │
│  │ dag_name: "data_ingestion_pipeline"          │ │
│  │ type: "bigquery"                              │ │
│  │ schedule: "@daily"                            │ │
│  │ environments:                                  │ │
│  │   dev: {dataset: "raw_data_dev"}              │ │
│  │   prod: {dataset: "raw_data_prod"}            │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Ação:** Mostrar Dockerfile, estrutura, YAML configs, UI de Configurações

---

## 🎯 Segmento 3: Tutorial Básico (10 min)

### Demo 01: DAG Simples (3 min)

```
┌─────────────────────────────────────────────────────┐
│  demo_01_simple_python                              │
│                                                      │
│  ┌─────────┐      ┌──────────┐      ┌───────────┐ │
│  │ Extract │ ───▶ │Transform │ ───▶ │   Load    │ │
│  │         │      │          │      │           │ │
│  │ Python  │      │  Python  │      │  Python   │ │
│  └─────────┘      └──────────┘      └───────────┘ │
│                                                      │
│  📥 Busca dados    🔄 Processa      💾 Salva       │
└─────────────────────────────────────────────────────┘
```

**Ação:** Executar DAG, ver logs, ver XCom

---

### Demo 02: Dependências Complexas (3 min)

```
┌─────────────────────────────────────────────────────┐
│  demo_02_task_dependencies                         │
│                                                      │
│              ┌───────┐                             │
│              │ Start │                             │
│              └───┬───┘                             │
│                  │                                 │
│        ┌──────────┴──────────┐                      │
│        │                     │                      │
│    ┌───▼────┐         ┌────▼───┐                  │
│    │Extract │         │Extract │                  │
│    │ Users  │         │Products│                  │
│    └───┬────┘         └────┬───┘                  │
│        │                  │                        │
│    ┌───▼────┐         ┌────▼───┐                  │
│    │Validate│         │Validate│                  │
│    │ Users  │         │Products│                  │
│    └───┬────┘         └────┬───┘                  │
│        │                  │                        │
│        └────────┬─────────┘                       │
│                 ▼                                  │
│          ┌─────────────┐                          │
│          │ Notification │                          │
│          └──────┬───────┘                          │
│                 ▼                                  │
│              ┌─────┐                               │
│              │ End │                               │
│              └─────┘                               │
└─────────────────────────────────────────────────────┘
```

**Ação:** Executar, mostrar paralelismo

---

### Demo 03: BigQuery (4 min)

```
┌─────────────────────────────────────────────────────┐
│  demo_03_bigquery                                   │
│                                                      │
│  ┌──────────────┐                                   │
│  │   Airflow    │                                   │
│  │              │                                   │
│  │  BigQuery    │                                   │
│  │  Operator    │                                   │
│  └──────┬───────┘                                   │
│         │                                           │
│         │ SQL Query                                 │
│         ▼                                           │
│  ┌──────────────────────────────────────┐          │
│  │        Google BigQuery                │          │
│  │  ┌──────────┐  ┌──────────┐          │          │
│  │  │ Tables   │  │ Queries  │          │          │
│  │  └──────────┘  └──────────┘          │          │
│  └──────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

**Ação:** Executar query, ver no BigQuery Console

---

## 🎯 Segmento 4: Data Engineering + ML (10 min)

### Pipeline Completo

```
┌─────────────────────────────────────────────────────┐
│  ML Pipeline End-to-End                             │
│                                                      │
│  ETL Phase                                          │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐         │
│  │ Extract │──▶│Transform │──▶│  Load    │         │
│  └─────────┘   └──────────┘   └──────────┘         │
│                                                      │
│  Feature Engineering                                 │
│  ┌──────────────────────────────┐                   │
│  │  Feature Creation            │                   │
│  │  • Age normalization         │                   │
│  │  • Income log                │                   │
│  │  • Score scaling             │                   │
│  └──────────────────────────────┘                   │
│                                                      │
│  ML Phase                                           │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Training │─▶│ Eval     │─▶│ Registry │         │
│  └───────────┘  └──────────┘  └──────────┘         │
│       │                                              │
│       ▼                                              │
│  ┌───────────┐                                      │
│  │  Deploy   │                                      │
│  └───────────┘                                      │
└─────────────────────────────────────────────────────┘
```

**Ação:** Executar pipeline completo, mostrar cada etapa

---

## 🎯 Segmento 5: Integração GCP (5 min)

### Arquitetura Completa

```
┌────────────────────────────────────────────────────┐
│              Astronomer Airflow                     │
│  ┌────────────────────────────────────────────┐    │
│  │              DAGs                          │    │
│  │  • data_ingestion_pipeline                 │    │
│  │  • ml_training_pipeline                    │    │
│  │  • model_inference_pipeline                │    │
│  └────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────┘
             │                │              │
             ▼                ▼              ▼
   ┌──────────────┐  ┌──────────────┐  ┌───────────────┐
   │  BigQuery    │  │  Dataproc    │  │ Vertex AI    │
   │              │  │              │  │              │
   │ • Storage    │  │ • Spark       │  │ • Training   │
   │ • Analytics  │  │ • PySpark    │  │ • Registry   │
   │ • ML Dataset  │  │ • Processing  │  │ • Deploy     │
   └──────────────┘  └──────────────┘  └───────────────┘
```

**Ação:** Mostrar integração com cada serviço GCP

---

## 🎯 Segmento 6: Q&A (2 min)

```
┌────────────────────────────────────────────────────┐
│  Recursos Adicionais                               │
│  ┌─────────────────────────────────────────────┐  │
│  │ • Astronomer Docs                            │  │
│  │ • Airflow Docs                               │  │
│  │ • GCP Integration                            │  │
│  │ • Astronomer Academy                         │  │
│  └─────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

**Ação:** Responder perguntas, compartilhar links

---

## 📊 Visão Geral dos DAGs

```
┌─────────────────────────────────────────────────────────────┐
│                    DAGs de Demonstração                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  demo_01_simple_python.py         ───▶ Conceitos básicos    │
│  demo_02_task_dependencies.py     ───▶ Dependências          │
│  demo_03_bigquery.py               ───▶ BigQuery              │
│  demo_04_ml_pipeline.py            ───▶ ML Pipeline          │
│  demo_05_dynamic_task_mapping.py   ───▶ Dynamic Tasks        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎬 Timeline Visual

```
Time    Segmento                    Ação
──────────────────────────────────────────────────────────
00:00 ─────────────────────────── ▶ Introdução
        (5 min)
        │
        ├─ O que é Astronomer?
        ├─ Visão geral
        └─ Mostrar UI

05:00 ─────────────────────────── ▶ Setup
        (8 min)
        │
        ├─ Docker
        ├─ Estrutura
        ├─ YAML configs
        └─ Observabilidade

13:00 ─────────────────────────── ▶ Tutorial Básico
        (10 min)
        │
        ├─ Demo 01: Simple (3 min)
        ├─ Demo 02: Dependencies (3 min)
        └─ Demo 03: BigQuery (4 min)

23:00 ─────────────────────────── ▶ Data Eng + ML
        (10 min)
        │
        ├─ Ingestão (3 min)
        ├─ Features (3 min)
        └─ Training (4 min)

33:00 ─────────────────────────── ▶ Integração GCP
        (5 min)
        │
        ├─ BigQuery (2 min)
        ├─ Dataproc (2 min)
        └─ Vertex AI (1 min)

38:00 ─────────────────────────── ▶ Q&A
        (2 min)
        │
        └─ Perguntas

40:00 ────────────────────────────────────────── ● FIM
```

---

## 🎯 Fluxo de Demonstração

```
Apresentação inicia
        ↓
[1] Introdução (5 min)
        ↓
[2] Setup (8 min)
        ↓
[3] Tutorial (10 min)
        ↓ demo_01, demo_02, demo_03
[4] Data Eng + ML (10 min)
        ↓ demo_04 + pipelines reais
[5] Integração GCP (5 min)
        ↓ BigQuery, Dataproc, Vertex AI
[6] Q&A (2 min)
        ↓
    Fim da Apresentação
```

---

## 📝 Checklist por Segmento

### Segmento 1-2: Introdução e Setup
- [ ] Apresentar Astronomer
- [ ] Mostrar UI
- [ ] Mostrar Dockerfile
- [ ] Mostrar estrutura
- [ ] Mostrar configs

### Segmento 3: Tutorial
- [ ] Executar demo_01
- [ ] Executar demo_02
- [ ] Executar demo_03
- [ ] Mostrar logs

### Segmento 4: ML
- [ ] Executar pipeline ingestão
- [ ] Executar pipeline ML
- [ ] Mostrar código
- [ ] Mostrar SQL

### Segmento 5: GCP
- [ ] Mostrar BigQuery
- [ ] Mostrar Dataproc
- [ ] Mostrar Vertex AI

### Segmento 6: Q&A
- [ ] Responder perguntas
- [ ] Compartilhar recursos

---

## 🎓 Conclusão

Esta estrutura visual fornece uma guia clara de como apresentar o Astronomer Airflow em 40 minutos, demonstrando conceitos essenciais de Data Engineering e Machine Learning na nuvem.

**Boa apresentação! 🚀**

