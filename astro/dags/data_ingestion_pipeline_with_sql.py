"""
Data ingestion pipeline for processing raw data from various sources into BigQuery

Generated BigQuery DAG: data_ingestion_pipeline
"""

from airflow.sdk import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.sensors.bigquery import BigQueryJobSensor
from pendulum import datetime
from typing import Any, Dict

# Default arguments
default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": "00:10:00",
    "email": ['data-team@company.com'],
    "email_on_failure": True,
    "email_on_retry": False
}

@dag(
    dag_id="data_ingestion_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    default_args=default_args,
    description="Data ingestion pipeline for processing raw data from various sources into BigQuery",
    tags=['ingestion', 'bigquery', 'data-pipeline'],
    catchup=False,
    max_active_runs=1
)
def data_ingestion_pipeline():
    extract_raw_data = BigQueryExecuteQueryOperator(
        task_id="extract_raw_data",
        sql="""-- Extract raw data from source tables
-- Environment parameters: {{ var.value.gcp_project_id }}, {{ var.value.bigquery_source_dataset }}, {{ var.value.bigquery_dataset_id }}, {{ ds }}

SELECT 
  *,
  CURRENT_TIMESTAMP() as ingestion_timestamp
FROM `{{ var.value.gcp_project_id }}.{{ var.value.bigquery_source_dataset }}.raw_data`
WHERE DATE(created_at) = '{{ ds }}'
""",
        destination_dataset_table="{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.raw_data_{{ ds_nodash }}",
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default"
    )
    validate_data_quality = BigQueryExecuteQueryOperator(
        task_id="validate_data_quality",
        sql="""-- Validate data quality and add quality status
-- Environment parameters: {{ var.value.gcp_project_id }}, {{ var.value.bigquery_dataset_id }}, {{ ds }}

SELECT 
  *,
  CASE 
    WHEN id IS NULL THEN 'MISSING_ID'
    WHEN email IS NULL OR email = '' THEN 'MISSING_EMAIL'
    WHEN created_at IS NULL THEN 'MISSING_TIMESTAMP'
    ELSE 'VALID'
  END as data_quality_status
FROM `{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.raw_data_{{ ds_nodash }}`
""",
        destination_dataset_table="{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.validated_data_{{ ds_nodash }}",
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default"
    )
    load_to_warehouse = BigQueryExecuteQueryOperator(
        task_id="load_to_warehouse",
        sql="""-- Load validated data to warehouse
-- Environment parameters: {{ var.value.gcp_project_id }}, {{ var.value.bigquery_dataset_id }}, {{ ds }}

INSERT INTO `{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.warehouse_data`
SELECT 
  id,
  email,
  name,
  created_at,
  ingestion_timestamp,
  data_quality_status
FROM `{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.validated_data_{{ ds_nodash }}`
WHERE data_quality_status = 'VALID'
""",
        write_disposition="WRITE_APPEND",
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default"
    )
    
    # Define task dependencies
    validate_data_quality >> extract_raw_data
    load_to_warehouse >> validate_data_quality

# Instantiate the DAG
data_ingestion_pipeline()