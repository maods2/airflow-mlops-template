-- Create combined features from user and product features
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

CREATE OR REPLACE TABLE `{project_id}.{target_dataset}.combined_features_{execution_date_nodash}`
AS
SELECT 
  uf.user_id,
  uf.total_events,
  uf.unique_event_types,
  uf.avg_session_duration,
  uf.user_status,
  pf.product_id,
  pf.total_views,
  pf.unique_viewers,
  pf.avg_rating,
  pf.conversion_rate,
  CURRENT_TIMESTAMP() as feature_created_at
FROM `{project_id}.{target_dataset}.user_features_{execution_date_nodash}` uf
CROSS JOIN `{project_id}.{target_dataset}.product_features_{execution_date_nodash}` pf
