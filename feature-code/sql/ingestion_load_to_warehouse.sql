-- Load validated data to warehouse
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

INSERT INTO `{project_id}.{target_dataset}.warehouse_data`
SELECT 
  id,
  email,
  name,
  created_at,
  ingestion_timestamp,
  data_quality_status
FROM `{project_id}.{target_dataset}.validated_data_{execution_date_nodash}`
WHERE data_quality_status = 'VALID'
