# Docker Setup for MLOps Airflow Framework

This document explains how to build and run the MLOps Airflow framework using Docker.

## Prerequisites

- Docker installed and running
- Access to the Astro Runtime base image

## Quick Start

### Build the Image

```bash
# Using the build script (recommended)
./build_docker.sh

# Or manually
docker build -f astro/Dockerfile -t airflow-mlops .
```

### Run the Container

```bash
# Basic run (generates DAGs and exits)
docker run --rm \
  -e GCP_PROJECT_ID="your-project-123" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="your-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data" \
  -e GCP_TARGET_DATASET="warehouse" \
  -e ENVIRONMENT="prod" \
  airflow-mlops

# Run with Airflow UI
docker run \
  -e GCP_PROJECT_ID="your-project-123" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="your-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data" \
  -e GCP_TARGET_DATASET="warehouse" \
  -e ENVIRONMENT="prod" \
  -p 8080:8080 \
  airflow-mlops astro dev start
```

## Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GCP_PROJECT_ID` | GCP Project ID | `my-project-123` | Yes |
| `GCP_REGION` | GCP Region | `us-central1` | Yes |
| `GCP_BUCKET_NAME` | GCS Bucket Name | `my-ml-bucket` | Yes |
| `GCP_SOURCE_DATASET` | Source BigQuery Dataset | `raw_data` | Yes |
| `GCP_TARGET_DATASET` | Target BigQuery Dataset | `warehouse` | Yes |
| `ENVIRONMENT` | Environment (dev/qa/prod) | `prod` | No (default: prod) |

## Build Process

The Docker build process:

1. **Base Image**: Uses Astro Runtime 3.1-2
2. **Dependencies**: Installs Python packages from requirements.txt
3. **Code Copy**: Copies DAG builder, templates, configs, and feature-code
4. **Environment Setup**: Sets default environment variables
5. **DAG Generation**: Runs DAG generation on container start

## Directory Structure in Container

```
/usr/local/airflow/
├── dag_builder/           # DAG builder module
├── templates/             # Jinja2 templates
├── config/                # YAML configurations
├── feature-code/          # SQL files and Python code
│   └── sql/              # SQL query files
├── dags/                 # Generated DAG files
└── generate_dags.py      # DAG generation script
```

## Development Workflow

### 1. Local Development

```bash
# Build the image
docker build -f astro/Dockerfile -t airflow-mlops .

# Test DAG generation
docker run --rm \
  -e GCP_PROJECT_ID="dev-project" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="dev-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_dev" \
  -e GCP_TARGET_DATASET="warehouse_dev" \
  -e ENVIRONMENT="dev" \
  airflow-mlops
```

### 2. Production Deployment

```bash
# Build for production
docker build -f astro/Dockerfile -t airflow-mlops:prod .

# Run in production
docker run -d \
  --name airflow-mlops-prod \
  -e GCP_PROJECT_ID="prod-project" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="prod-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_prod" \
  -e GCP_TARGET_DATASET="warehouse_prod" \
  -e ENVIRONMENT="prod" \
  -p 8080:8080 \
  airflow-mlops:prod astro dev start
```

## Troubleshooting

### Common Issues

1. **Build Context Error**
   ```
   ERROR: failed to solve: failed to compute cache key: "/feature-code": not found
   ```
   **Solution**: Build from the root directory, not from the astro/ directory

2. **Permission Denied**
   ```
   chmod: changing permissions: Operation not permitted
   ```
   **Solution**: The Dockerfile no longer uses chmod commands

3. **SQL Files Not Found**
   ```
   [Errno 2] No such file or directory: '../feature-code/sql'
   ```
   **Solution**: Updated DAG builder to use correct paths

4. **Environment Variables Not Set**
   ```
   Environment variable injection failed
   ```
   **Solution**: Ensure all required environment variables are set

### Debug Mode

```bash
# Run with debug output
docker run --rm \
  -e GCP_PROJECT_ID="test-project" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="test-bucket" \
  -e GCP_SOURCE_DATASET="raw_data" \
  -e GCP_TARGET_DATASET="warehouse" \
  -e ENVIRONMENT="prod" \
  airflow-mlops python -c "
import os
print('Environment variables:')
for key, value in os.environ.items():
    if key.startswith('GCP_'):
        print(f'  {key}: {value}')
"
```

## Multi-Environment Setup

### Development Environment
```bash
docker run --rm \
  -e GCP_PROJECT_ID="dev-project-123" \
  -e GCP_REGION="us-central1" \
  -e GCP_BUCKET_NAME="dev-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_dev" \
  -e GCP_TARGET_DATASET="warehouse_dev" \
  -e ENVIRONMENT="dev" \
  airflow-mlops
```

### QA Environment
```bash
docker run --rm \
  -e GCP_PROJECT_ID="qa-project-456" \
  -e GCP_REGION="us-west1" \
  -e GCP_BUCKET_NAME="qa-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_qa" \
  -e GCP_TARGET_DATASET="warehouse_qa" \
  -e ENVIRONMENT="qa" \
  airflow-mlops
```

### Production Environment
```bash
docker run --rm \
  -e GCP_PROJECT_ID="prod-project-789" \
  -e GCP_REGION="us-east1" \
  -e GCP_BUCKET_NAME="prod-ml-bucket" \
  -e GCP_SOURCE_DATASET="raw_data_prod" \
  -e GCP_TARGET_DATASET="warehouse_prod" \
  -e ENVIRONMENT="prod" \
  airflow-mlops
```

## Docker Compose (Optional)

Create a `docker-compose.yml` for easier management:

```yaml
version: '3.8'
services:
  airflow-mlops:
    build:
      context: .
      dockerfile: astro/Dockerfile
    environment:
      - GCP_PROJECT_ID=${GCP_PROJECT_ID}
      - GCP_REGION=${GCP_REGION}
      - GCP_BUCKET_NAME=${GCP_BUCKET_NAME}
      - GCP_SOURCE_DATASET=${GCP_SOURCE_DATASET}
      - GCP_TARGET_DATASET=${GCP_TARGET_DATASET}
      - ENVIRONMENT=${ENVIRONMENT:-prod}
    ports:
      - "8080:8080"
    command: ["astro", "dev", "start"]
```

Usage:
```bash
# Set environment variables
export GCP_PROJECT_ID="your-project"
export GCP_REGION="us-central1"
export GCP_BUCKET_NAME="your-bucket"
export GCP_SOURCE_DATASET="raw_data"
export GCP_TARGET_DATASET="warehouse"
export ENVIRONMENT="prod"

# Run with docker-compose
docker-compose up
```

## Best Practices

1. **Always build from root directory** to include feature-code
2. **Set all required environment variables** before running
3. **Use specific image tags** for production deployments
4. **Mount volumes** for persistent data if needed
5. **Use secrets management** for sensitive environment variables
6. **Monitor container logs** for DAG generation status

## Security Considerations

1. **Environment Variables**: Use Docker secrets for sensitive values
2. **Image Scanning**: Regularly scan images for vulnerabilities
3. **Network Security**: Use appropriate network configurations
4. **Access Control**: Implement proper access controls for GCP resources

This Docker setup provides a complete, containerized MLOps Airflow framework that can be easily deployed across different environments.
