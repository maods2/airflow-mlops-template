-- Extract raw data from source tables
-- Environment parameters: {project_id}, {source_dataset}, {target_dataset}, {execution_date}

SELECT 
  *,
  CURRENT_TIMESTAMP() as ingestion_timestamp
FROM `{project_id}.{source_dataset}.raw_data`
WHERE DATE(created_at) = '{execution_date}'
