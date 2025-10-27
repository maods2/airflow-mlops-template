-- Create warehouse_data table for processed data
-- Environment parameters: {project_id}, {target_dataset}

CREATE TABLE IF NOT EXISTS `{project_id}.{target_dataset}.warehouse_data` (
  id STRING NOT NULL,
  email STRING,
  name STRING,
  created_at TIMESTAMP,
  ingestion_timestamp TIMESTAMP,
  data_quality_status STRING,
  -- Add additional fields as needed
  metadata JSON
)
PARTITION BY DATE(created_at)
CLUSTER BY id
OPTIONS(
  description="Warehouse table for processed and validated data"
);
