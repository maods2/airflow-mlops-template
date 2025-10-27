-- Validate training data and generate statistics
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT id) as unique_ids,
  COUNT(CASE WHEN target_value IS NULL THEN 1 END) as missing_targets,
  MIN(created_at) as earliest_date,
  MAX(created_at) as latest_date
FROM `{project_id}.{target_dataset}.training_data_{execution_date_nodash}`
