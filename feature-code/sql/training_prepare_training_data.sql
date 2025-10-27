-- Prepare training data by joining features with labels
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

CREATE OR REPLACE TABLE `{project_id}.{target_dataset}.training_data_{execution_date_nodash}`
AS
SELECT 
  features.*,
  labels.target_value
FROM `{project_id}.{target_dataset}.warehouse_data` features
JOIN `{project_id}.{target_dataset}.labels` labels
ON features.id = labels.id
WHERE DATE(features.created_at) BETWEEN DATE_SUB('{execution_date}', INTERVAL 30 DAY) AND '{execution_date}'
