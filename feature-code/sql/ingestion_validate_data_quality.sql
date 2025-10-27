-- Validate data quality and add quality status
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

SELECT 
  *,
  CASE 
    WHEN id IS NULL THEN 'MISSING_ID'
    WHEN email IS NULL OR email = '' THEN 'MISSING_EMAIL'
    WHEN created_at IS NULL THEN 'MISSING_TIMESTAMP'
    ELSE 'VALID'
  END as data_quality_status
FROM `{project_id}.{target_dataset}.raw_data_{execution_date_nodash}`
