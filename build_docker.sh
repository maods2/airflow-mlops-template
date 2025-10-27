#!/bin/bash
# Build script for Docker image with proper context

echo "Building MLOps Airflow Docker image..."

# Build from the root directory to include feature-code
docker build -f astro/Dockerfile -t airflow-mlops .

echo "Build completed successfully!"
echo ""
echo "To run the container:"
echo "docker run -e GCP_PROJECT_ID='your-project' -e GCP_REGION='us-central1' -e GCP_BUCKET_NAME='your-bucket' -e GCP_SOURCE_DATASET='raw_data' -e GCP_TARGET_DATASET='warehouse' -e ENVIRONMENT='prod' -p 8080:8080 airflow-mlops"
echo ""
echo "To run with Airflow UI:"
echo "docker run -e GCP_PROJECT_ID='your-project' -e GCP_REGION='us-central1' -e GCP_BUCKET_NAME='your-bucket' -e GCP_SOURCE_DATASET='raw_data' -e GCP_TARGET_DATASET='warehouse' -e ENVIRONMENT='prod' -p 8080:8080 airflow-mlops astro dev start"
