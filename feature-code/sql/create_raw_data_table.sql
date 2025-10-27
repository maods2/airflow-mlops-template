-- Create raw_data table for data ingestion
-- Environment parameters: {project_id}, {source_dataset}

CREATE TABLE IF NOT EXISTS `{project_id}.{source_dataset}.raw_data` (
  id STRING NOT NULL,
  email STRING,
  name STRING,
  created_at TIMESTAMP,
  -- Additional fields as needed
  metadata JSON
)
PARTITION BY DATE(created_at)
OPTIONS(
  description="Raw data table for ingestion pipeline"
);
