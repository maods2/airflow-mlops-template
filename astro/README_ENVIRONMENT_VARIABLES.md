# Environment Variables Architecture

This document explains the environment variables architecture implemented in the MLOps framework, where project IDs, regions, and bucket names are handled at the Docker/template level instead of being hardcoded in YAML configurations.

## Overview

The framework now uses environment variables to manage infrastructure-specific parameters, providing better separation of concerns and easier deployment across different environments.

## Architecture

```
Docker Level (Environment Variables)
├── GCP_PROJECT_ID          # GCP Project ID
├── GCP_REGION             # GCP Region
├── GCP_BUCKET_NAME        # GCS Bucket Name
├── GCP_SOURCE_DATASET     # Source BigQuery Dataset
├── GCP_TARGET_DATASET     # Target BigQuery Dataset
└── ENVIRONMENT            # Environment (dev/qa/prod)

YAML Config Level (Business Logic Only)
├── dataset_id             # Environment-specific dataset names
├── cluster_name           # Environment-specific cluster names
└── sql_file               # SQL file references

Template Level (Parameter Injection)
├── Environment variable reading
├── Parameter injection into SQL
└── DAG generation with injected values
```

## Environment Variables

### Required Environment Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| `GCP_PROJECT_ID` | GCP Project ID | `my-project-123` | `{{ var.value.gcp_project_id }}` |
| `GCP_REGION` | GCP Region | `us-central1` | `{{ var.value.gcp_region }}` |
| `GCP_BUCKET_NAME` | GCS Bucket Name | `my-ml-bucket` | `{project_id}-ml-bucket` |
| `GCP_SOURCE_DATASET` | Source Dataset | `raw_data` | `{{ var.value.bigquery_source_dataset }}` |
| `GCP_TARGET_DATASET` | Target Dataset | `warehouse` | `{{ var.value.bigquery_dataset_id }}` |
| `ENVIRONMENT` | Environment | `prod` | `prod` |

### Docker Configuration

The Dockerfile sets default environment variables:

```dockerfile
# Set environment variables for GCP configuration
# These can be overridden at runtime
ENV GCP_PROJECT_ID=""
ENV GCP_REGION="us-central1"
ENV GCP_BUCKET_NAME=""
ENV GCP_SOURCE_DATASET="raw_data"
ENV GCP_TARGET_DATASET="warehouse"
ENV ENVIRONMENT="prod"
```

## YAML Configuration Structure

YAML files now only contain business logic parameters:

### Before (Hardcoded Infrastructure)
```yaml
environments:
  dev:
    project_id: "dev-project-123"
    region: "us-central1"
    bucket_name: "dev-ml-bucket"
    dataset_id: "warehouse_dev"
  prod:
    project_id: "{{ var.value.gcp_project_id }}"
    region: "{{ var.value.gcp_region }}"
    bucket_name: "{{ var.value.gcp_project_id }}-ml-bucket"
    dataset_id: "{{ var.value.bigquery_dataset_id }}"
```

### After (Environment Variables)
```yaml
environments:
  dev:
    dataset_id: "warehouse_dev"
    cluster_name: "ml-cluster-dev"
  qa:
    dataset_id: "warehouse_qa"
    cluster_name: "ml-cluster-qa"
  prod:
    dataset_id: "warehouse_prod"
    cluster_name: "ml-cluster"
```

## Parameter Injection

### SQL File Parameters

SQL files use placeholders that are replaced with environment variables:

```sql
-- feature-code/sql/my_query.sql
-- Parameters: {project_id}, {target_dataset}, {execution_date}

SELECT 
  id,
  name,
  created_at
FROM `{project_id}.{target_dataset}.my_table`
WHERE DATE(created_at) = '{execution_date}'
```

### DAG Template Parameters

DAG templates receive environment variables directly:

```python
# Generated DAG content
project_id = "my-project-123"  # From GCP_PROJECT_ID
region = "us-central1"         # From GCP_REGION
bucket_name = "my-ml-bucket"   # From GCP_BUCKET_NAME
```

## Deployment Examples

### Development Environment
```bash
docker run -e GCP_PROJECT_ID="dev-project-123" \
           -e GCP_REGION="us-central1" \
           -e GCP_BUCKET_NAME="dev-ml-bucket" \
           -e GCP_SOURCE_DATASET="raw_data_dev" \
           -e GCP_TARGET_DATASET="warehouse_dev" \
           -e ENVIRONMENT="dev" \
           my-airflow-mlops
```

### QA Environment
```bash
docker run -e GCP_PROJECT_ID="qa-project-456" \
           -e GCP_REGION="us-west1" \
           -e GCP_BUCKET_NAME="qa-ml-bucket" \
           -e GCP_SOURCE_DATASET="raw_data_qa" \
           -e GCP_TARGET_DATASET="warehouse_qa" \
           -e ENVIRONMENT="qa" \
           my-airflow-mlops
```

### Production Environment
```bash
docker run -e GCP_PROJECT_ID="prod-project-789" \
           -e GCP_REGION="us-east1" \
           -e GCP_BUCKET_NAME="prod-ml-bucket" \
           -e GCP_SOURCE_DATASET="raw_data_prod" \
           -e GCP_TARGET_DATASET="warehouse_prod" \
           -e ENVIRONMENT="prod" \
           my-airflow-mlops
```

## DAG Builder Updates

The DAG builder now reads environment variables:

```python
def load_sql_file(self, sql_file: str, environment: str = "prod") -> str:
    # Get environment variables
    gcp_project_id = os.getenv('GCP_PROJECT_ID', '{{ var.value.gcp_project_id }}')
    gcp_region = os.getenv('GCP_REGION', '{{ var.value.gcp_region }}')
    gcp_bucket_name = os.getenv('GCP_BUCKET_NAME', f'{gcp_project_id}-ml-bucket')
    gcp_source_dataset = os.getenv('GCP_SOURCE_DATASET', '{{ var.value.bigquery_source_dataset }}')
    gcp_target_dataset = os.getenv('GCP_TARGET_DATASET', '{{ var.value.bigquery_dataset_id }}')
    
    # Inject parameters into SQL
    params = {
        'project_id': gcp_project_id,
        'source_dataset': gcp_source_dataset,
        'target_dataset': gcp_target_dataset,
        'bucket_name': gcp_bucket_name,
        'region': gcp_region
    }
    
    for key, value in params.items():
        sql_content = sql_content.replace(f'{{{key}}}', value)
    
    return sql_content
```

## Benefits

### 1. **Separation of Concerns**
- Infrastructure parameters managed at Docker level
- Business logic parameters in YAML configs
- Clear separation between deployment and configuration

### 2. **Environment Management**
- Easy switching between environments
- No hardcoded values in configuration files
- Consistent parameter injection across all DAGs

### 3. **Security**
- Sensitive values not stored in version control
- Environment-specific secrets managed externally
- Reduced risk of accidental exposure

### 4. **Deployment Flexibility**
- Same configuration files for all environments
- Environment-specific values injected at runtime
- Easy to add new environments

### 5. **Maintainability**
- Single source of truth for infrastructure parameters
- Easier to update project IDs, regions, etc.
- Reduced configuration duplication

## Migration Guide

### From Hardcoded to Environment Variables

1. **Remove hardcoded values** from YAML configs:
   ```yaml
   # Remove these
   project_id: "dev-project-123"
   region: "us-central1"
   bucket_name: "dev-ml-bucket"
   ```

2. **Keep business logic parameters**:
   ```yaml
   # Keep these
   dataset_id: "warehouse_dev"
   cluster_name: "ml-cluster-dev"
   ```

3. **Set environment variables** in Docker:
   ```dockerfile
   ENV GCP_PROJECT_ID="my-project"
   ENV GCP_REGION="us-central1"
   ENV GCP_BUCKET_NAME="my-bucket"
   ```

4. **Update deployment scripts** to pass environment variables

## Testing

The framework includes comprehensive tests for environment variables:

```bash
# Run environment variable tests
python test_env_variables.py
```

Tests cover:
- Environment variable loading
- Parameter injection into SQL files
- DAG generation with environment variables
- Configuration validation

## Best Practices

1. **Environment Variables**: Set all required environment variables
2. **Default Values**: Provide sensible defaults in Dockerfile
3. **Validation**: Validate environment variables at startup
4. **Documentation**: Document all environment variables
5. **Security**: Use secrets management for sensitive values

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**: Check Docker environment variable settings
2. **Parameter Not Injected**: Verify environment variable names
3. **Wrong Values**: Check environment variable values
4. **Template Errors**: Verify template parameter usage

### Debug Mode

Enable debug logging to see parameter injection:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Example: Complete Deployment

```bash
# Build the image
docker build -t my-airflow-mlops .

# Run with environment variables
docker run -d \
  --name airflow-mlops \
  -e GCP_PROJECT_ID="my-production-project" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="my-production-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_prod" \
  -e GCP_TARGET_DATASET="warehouse_prod" \
  -e ENVIRONMENT="prod" \
  -p 8080:8080 \
  my-airflow-mlops
```

This architecture provides a clean separation between infrastructure configuration and business logic, making the MLOps framework more maintainable and deployment-friendly.
