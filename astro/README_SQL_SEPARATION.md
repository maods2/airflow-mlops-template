# SQL Separation Architecture

This document explains the SQL separation architecture implemented in the MLOps framework, where SQL queries are stored in separate files and environment parameters are injected from YAML configurations.

## Overview

The framework now separates SQL queries from YAML configuration files, providing better maintainability, version control, and environment-specific parameter injection.

## Architecture

```
feature-code/
└── sql/                          # SQL query files
    ├── ingestion_extract_raw_data.sql
    ├── ingestion_validate_data_quality.sql
    ├── ingestion_load_to_warehouse.sql
    ├── training_prepare_training_data.sql
    ├── training_validate_training_data.sql
    ├── feature_engineering_create_user_features.sql
    ├── feature_engineering_create_product_features.sql
    └── feature_engineering_create_combined_features.sql

astro/
├── config/                       # YAML configuration files
│   ├── ingestion.yaml           # Environment parameters only
│   ├── training.yaml
│   ├── feature_engineering.yaml
│   └── model_inference.yaml
└── dag_builder/                 # DAG builder with SQL loading
    ├── builder.py               # Updated with SQL file loading
    ├── config_loader.py         # Updated schema for SQL files
    └── templates.py
```

## SQL File Structure

SQL files are stored in `feature-code/sql/` and use parameter placeholders for environment-specific values:

```sql
-- Example: ingestion_extract_raw_data.sql
-- Environment parameters: {project_id}, {source_dataset}, {target_dataset}, {execution_date}

SELECT 
  *,
  CURRENT_TIMESTAMP() as ingestion_timestamp
FROM `{project_id}.{source_dataset}.raw_data`
WHERE DATE(created_at) = '{execution_date}'
```

### Parameter Placeholders

- `{project_id}` - GCP Project ID
- `{source_dataset}` - Source BigQuery dataset
- `{target_dataset}` - Target BigQuery dataset
- `{execution_date}` - Airflow execution date ({{ ds }})
- `{execution_date_nodash}` - Execution date without dashes ({{ ds_nodash }})
- `{bucket_name}` - GCS bucket name for Dataproc jobs

## YAML Configuration Structure

YAML files now only contain environment-specific parameters and references to SQL files:

```yaml
# Example: ingestion.yaml
dag_name: "data_ingestion_pipeline"
type: "bigquery"
description: "Data ingestion pipeline"

# Environment-specific parameters
environments:
  dev:
    project_id: "dev-project-123"
    source_dataset: "raw_data_dev"
    target_dataset: "warehouse_dev"
  qa:
    project_id: "qa-project-456"
    source_dataset: "raw_data_qa"
    target_dataset: "warehouse_qa"
  prod:
    project_id: "{{ var.value.gcp_project_id }}"
    source_dataset: "{{ var.value.bigquery_source_dataset }}"
    target_dataset: "{{ var.value.bigquery_dataset_id }}"

queries:
  - task_id: "extract_raw_data"
    sql_file: "ingestion_extract_raw_data.sql"  # Reference to SQL file
    destination_table: "raw_data_{{ ds_nodash }}"
    write_disposition: "WRITE_TRUNCATE"
```

## DAG Builder Updates

The DAG builder has been updated to:

1. **Load SQL Files**: Read SQL content from `feature-code/sql/` directory
2. **Inject Parameters**: Replace placeholders with environment-specific values
3. **Support Both Modes**: Handle both inline SQL and SQL file references

### Key Methods

```python
# Load SQL file with parameter injection
sql_content = builder.load_sql_file("ingestion_extract_raw_data.sql")

# Get environment-specific parameters
env_params = builder.get_environment_params(config, "dev")

# Generate DAG with SQL file loading
dag_content = builder._generate_dag_content(config)
```

## Environment Management

### Development Environment
```yaml
environments:
  dev:
    project_id: "dev-project-123"
    source_dataset: "raw_data_dev"
    target_dataset: "warehouse_dev"
    region: "us-central1"
    cluster_name: "ml-cluster-dev"
    bucket_name: "dev-ml-bucket"
```

### QA Environment
```yaml
environments:
  qa:
    project_id: "qa-project-456"
    source_dataset: "raw_data_qa"
    target_dataset: "warehouse_qa"
    region: "us-central1"
    cluster_name: "ml-cluster-qa"
    bucket_name: "qa-ml-bucket"
```

### Production Environment
```yaml
environments:
  prod:
    project_id: "{{ var.value.gcp_project_id }}"
    source_dataset: "{{ var.value.bigquery_source_dataset }}"
    target_dataset: "{{ var.value.bigquery_dataset_id }}"
    region: "{{ var.value.gcp_region }}"
    cluster_name: "ml-cluster-prod"
    bucket_name: "{{ var.value.gcp_project_id }}-ml-bucket"
```

## Benefits

### 1. **Separation of Concerns**
- SQL logic separated from configuration
- Environment parameters centralized
- Better maintainability

### 2. **Version Control**
- SQL files can be versioned independently
- Easier to track changes to business logic
- Better code review process

### 3. **Environment Management**
- Easy switching between environments
- Consistent parameter injection
- Reduced configuration duplication

### 4. **Reusability**
- SQL files can be reused across different DAGs
- Parameter injection makes queries flexible
- Easier to test SQL logic independently

### 5. **Developer Experience**
- SQL files can be edited with proper syntax highlighting
- Better IDE support for SQL files
- Easier debugging and testing

## Usage Examples

### Creating a New SQL Query

1. **Create SQL file** in `feature-code/sql/`:
```sql
-- my_new_query.sql
SELECT 
  id,
  name,
  created_at
FROM `{project_id}.{target_dataset}.my_table`
WHERE DATE(created_at) = '{execution_date}'
```

2. **Reference in YAML**:
```yaml
queries:
  - task_id: "my_new_task"
    sql_file: "my_new_query.sql"
    destination_table: "my_results_{{ ds_nodash }}"
    write_disposition: "WRITE_TRUNCATE"
```

### Environment-Specific Deployment

```bash
# Deploy to development
ENVIRONMENT=dev python generate_dags.py

# Deploy to production
ENVIRONMENT=prod python generate_dags.py
```

## Migration Guide

### From Inline SQL to SQL Files

1. **Extract SQL** from YAML configuration
2. **Create SQL file** in `feature-code/sql/`
3. **Replace `sql:` with `sql_file:`** in YAML
4. **Add parameter placeholders** in SQL file
5. **Test with different environments**

### Example Migration

**Before:**
```yaml
queries:
  - task_id: "extract_data"
    sql: |
      SELECT * FROM `project.dataset.table`
      WHERE date = '{{ ds }}'
```

**After:**
```yaml
queries:
  - task_id: "extract_data"
    sql_file: "extract_data.sql"
```

```sql
-- extract_data.sql
SELECT * FROM `{project_id}.{target_dataset}.table`
WHERE date = '{execution_date}'
```

## Testing

The framework includes comprehensive tests for SQL separation:

```bash
# Run SQL separation tests
python test_sql_separation.py
```

Tests cover:
- SQL file loading
- Parameter injection
- Environment parameter extraction
- DAG generation with SQL files

## Best Practices

1. **Naming Convention**: Use descriptive names for SQL files
2. **Parameter Documentation**: Document all parameters in SQL file headers
3. **Environment Consistency**: Ensure all environments have required parameters
4. **SQL Validation**: Test SQL files with different parameter values
5. **Version Control**: Commit SQL files separately from DAG configurations

## Troubleshooting

### Common Issues

1. **SQL File Not Found**: Check file path in `feature-code/sql/`
2. **Parameter Not Injected**: Verify parameter name in SQL file
3. **Environment Not Found**: Check environment configuration in YAML
4. **Invalid SQL**: Test SQL with actual parameter values

### Debug Mode

Enable debug logging to see parameter injection:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This architecture provides a clean separation between SQL business logic and environment configuration, making the MLOps framework more maintainable and flexible.
