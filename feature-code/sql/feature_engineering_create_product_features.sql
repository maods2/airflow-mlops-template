-- Create product features from interactions data
-- Environment parameters: {project_id}, {target_dataset}, {execution_date}

CREATE OR REPLACE TABLE `{project_id}.{target_dataset}.product_features_{execution_date_nodash}`
AS
SELECT 
  product_id,
  COUNT(*) as total_views,
  COUNT(DISTINCT user_id) as unique_viewers,
  AVG(rating) as avg_rating,
  COUNT(CASE WHEN action = 'purchase' THEN 1 END) as total_purchases,
  COUNT(CASE WHEN action = 'purchase' THEN 1 END) / COUNT(*) as conversion_rate
FROM `{project_id}.{target_dataset}.product_interactions`
WHERE DATE(interaction_timestamp) = '{execution_date}'
GROUP BY product_id
