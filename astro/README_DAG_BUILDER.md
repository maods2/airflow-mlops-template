# DAG Builder Module

This module provides functionality to dynamically generate Airflow DAGs based on YAML configuration files and Jinja2 templates.

## Overview

The DAG Builder is designed to:
- Generate DAGs dynamically from YAML configuration files
- Support multiple DAG types (BigQuery, Dataproc, Hybrid)
- Use Jinja2 templates for flexible DAG generation
- Integrate with GCP services (BigQuery, Dataproc)
- Support complex task dependencies

## Architecture

```
astro/
├── dag_builder/           # DAG builder module
│   ├── __init__.py
│   ├── builder.py         # Main DAG builder class
│   ├── config_loader.py   # YAML configuration loader
│   └── templates.py       # Jinja2 template manager
├── templates/             # Jinja2 templates
│   ├── basic_dag.py.j2
│   ├── bigquery_dag.py.j2
│   ├── dataproc_dag.py.j2
│   └── hybrid_dag.py.j2
├── config/                # YAML configuration files
│   ├── ingestion.yaml
│   ├── training.yaml
│   ├── feature_engineering.yaml
│   └── model_inference.yaml
└── dags/                  # Generated DAG files
```

## Configuration File Structure

### SQL Separation Architecture

The framework now separates SQL queries from YAML configurations:

- **SQL Files**: Stored in `feature-code/sql/` with parameter placeholders
- **YAML Configs**: Contain only environment parameters and SQL file references
- **Parameter Injection**: Environment-specific values injected at runtime

### Basic DAG Configuration

```yaml
dag_name: "my_dag"
type: "basic"
description: "Description of the DAG"
schedule: "@daily"
start_date: "2024, 1, 1"

default_args:
  owner: "data_team"
  retries: 2
  retry_delay: "00:10:00"
  email: ["team@company.com"]
  email_on_failure: true

tags: ["tag1", "tag2"]

tasks:
  - task_id: "task1"
    type: "python"
    description: "Python task description"
  - task_id: "task2"
    type: "bash"
    bash_command: "echo 'Hello World'"
    depends_on: ["task1"]
```

### BigQuery DAG Configuration with SQL Files

```yaml
dag_name: "bigquery_dag"
type: "bigquery"
description: "BigQuery processing DAG"
schedule: "@daily"
start_date: "2024, 1, 1"

# Environment-specific parameters
environments:
  dev:
    project_id: "dev-project-123"
    dataset_id: "warehouse_dev"
  prod:
    project_id: "{{ var.value.gcp_project_id }}"
    dataset_id: "{{ var.value.bigquery_dataset_id }}"

queries:
  - task_id: "query1"
    sql_file: "my_query.sql"  # Reference to SQL file
    destination_table: "result_table"
    write_disposition: "WRITE_TRUNCATE"
  - task_id: "query2"
    sql_file: "count_query.sql"
    depends_on: ["query1"]
```

### SQL File Example

```sql
-- feature-code/sql/my_query.sql
-- Parameters: {project_id}, {dataset_id}, {execution_date}

SELECT 
  id,
  name,
  created_at
FROM `{project_id}.{dataset_id}.my_table`
WHERE DATE(created_at) = '{execution_date}'
```

### Dataproc DAG Configuration

```yaml
dag_name: "dataproc_dag"
type: "dataproc"
description: "Dataproc processing DAG"
schedule: "@daily"
start_date: "2024, 1, 1"

project_id: "{{ var.value.gcp_project_id }}"
region: "{{ var.value.gcp_region }}"
cluster_name: "my-cluster"

jobs:
  - task_id: "spark_job"
    job_type: "pyspark"
    main_python_file_uri: "gs://my-bucket/scripts/my_script.py"
    args: ["--input", "gs://my-bucket/input", "--output", "gs://my-bucket/output"]
```

### Hybrid DAG Configuration

```yaml
dag_name: "hybrid_dag"
type: "hybrid"
description: "Hybrid BigQuery + Dataproc DAG"
schedule: "@daily"
start_date: "2024, 1, 1"

project_id: "{{ var.value.gcp_project_id }}"
dataset_id: "{{ var.value.bigquery_dataset_id }}"
region: "{{ var.value.gcp_region }}"
cluster_name: "hybrid-cluster"

bigquery_tasks:
  - task_id: "prepare_data"
    sql: "SELECT * FROM source_table"
    destination_table: "prepared_data"

dataproc_tasks:
  - task_id: "process_data"
    job_type: "pyspark"
    main_python_file_uri: "gs://my-bucket/process.py"
    depends_on: ["prepare_data"]
```

## Usage

### Manual DAG Generation

```python
from dag_builder.builder import DAGBuilder

# Initialize builder
builder = DAGBuilder(
    config_dir="config",
    templates_dir="templates",
    dags_dir="dags"
)

# Generate single DAG
dag_path = builder.build_dag_from_config("ingestion.yaml")

# Generate all DAGs
generated_dags = builder.build_all_dags()
```

### Docker-based Generation

The Dockerfile automatically generates DAGs when the container starts:

```bash
# Build the image
docker build -t my-airflow-mlops .

# Run the container (DAGs will be generated automatically)
docker run my-airflow-mlops
```

### Using the Generation Script

```bash
# Run the generation script directly
python generate_dags.py
```

## Template Variables

Templates support the following variables:

### Airflow Variables
- `{{ var.value.gcp_project_id }}` - GCP Project ID
- `{{ var.value.bigquery_dataset_id }}` - BigQuery Dataset ID
- `{{ var.value.gcp_region }}` - GCP Region

### Airflow Macros
- `{{ ds }}` - Execution date (YYYY-MM-DD)
- `{{ ds_nodash }}` - Execution date (YYYYMMDD)
- `{{ ts }}` - Execution timestamp
- `{{ ts_nodash }}` - Execution timestamp (no dashes)

### Configuration Variables
- `{{ dag_name }}` - DAG name from config
- `{{ description }}` - DAG description
- `{{ schedule }}` - DAG schedule
- `{{ start_date }}` - DAG start date
- `{{ project_id }}` - GCP Project ID
- `{{ dataset_id }}` - BigQuery Dataset ID
- `{{ region }}` - GCP Region

## Custom Templates

You can create custom Jinja2 templates by:

1. Adding new template files to the `templates/` directory
2. Extending the `TemplateManager` class
3. Adding new DAG types to the `DAGBuilder` class

## Error Handling

The DAG builder includes comprehensive error handling:

- Configuration validation using JSON Schema
- Template rendering error handling
- File system error handling
- DAG generation error reporting

## Best Practices

1. **Configuration Files**: Keep configuration files focused on a single pipeline
2. **Templates**: Use descriptive variable names in templates
3. **Dependencies**: Define clear task dependencies in configuration
4. **Error Handling**: Include proper error handling in your Python scripts
5. **Resource Management**: Configure appropriate cluster sizes for Dataproc jobs
6. **Monitoring**: Use appropriate tags and email notifications

## Troubleshooting

### Common Issues

1. **Template Not Found**: Ensure template files exist in the `templates/` directory
2. **Configuration Validation Error**: Check YAML syntax and required fields
3. **Import Errors**: Ensure all dependencies are installed
4. **Permission Errors**: Check file permissions for DAG directory

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG
```

## Examples

See the `config/` directory for example configuration files:
- `ingestion.yaml` - Data ingestion pipeline
- `training.yaml` - ML training pipeline
- `feature_engineering.yaml` - Feature engineering pipeline
- `model_inference.yaml` - Model inference pipeline
