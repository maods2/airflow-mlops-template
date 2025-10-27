FROM astrocrpublic.azurecr.io/runtime:3.1-2
USER root
# Copy DAG builder module
COPY dag_builder/ /usr/local/airflow/dag_builder/

# Copy templates
COPY templates/ /usr/local/airflow/templates/

# Copy config files
COPY config/ /usr/local/airflow/config/

# Copy DAG generation script
COPY generate_dags.py /usr/local/airflow/generate_dags.py

# Set environment variables for GCP configuration
# These can be overridden at runtime
ENV GCP_PROJECT_ID="project-id"
ENV GCP_REGION="us-central1"
ENV GCP_BUCKET_NAME="bucket-name"
ENV GCP_SOURCE_DATASET="raw_data"
ENV GCP_TARGET_DATASET="warehouse"
ENV ENVIRONMENT="prod"

# Create feature-code directory
RUN mkdir -p /usr/local/airflow/feature-code


# Copy feature-code if it exists
COPY feature-code/ /usr/local/airflow/feature-code/

# Run DAG generation on container start
