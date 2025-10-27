-- Create user features from events data
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

CREATE OR REPLACE TABLE `{project_id}.{target_dataset}.user_features_{execution_date_nodash}`
AS
SELECT 
  user_id,
  COUNT(*) as total_events,
  COUNT(DISTINCT event_type) as unique_event_types,
  AVG(session_duration) as avg_session_duration,
  MAX(event_timestamp) as last_activity,
  DATE_DIFF(CURRENT_DATE(), DATE(MAX(event_timestamp)), DAY) as days_since_last_activity,
  CASE 
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(MAX(event_timestamp)), DAY) <= 7 THEN 'active'
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(MAX(event_timestamp)), DAY) <= 30 THEN 'inactive'
    ELSE 'dormant'
  END as user_status
FROM `{project_id}.{target_dataset}.user_events`
WHERE DATE(event_timestamp) = '{execution_date}'
GROUP BY user_id
