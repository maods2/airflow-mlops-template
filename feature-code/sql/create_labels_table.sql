-- Create labels table for ML training
-- Environment parameters: {project_id}, {target_dataset}

CREATE TABLE IF NOT EXISTS `{project_id}.{target_dataset}.labels` (
  id STRING NOT NULL,
  target_value FLOAT64,
  label_category STRING,
  label_created_at TIMESTAMP,
  metadata JSON
)
PARTITION BY DATE(label_created_at)
CLUSTER BY id
OPTIONS(
  description="Labels table for ML model training"
);
