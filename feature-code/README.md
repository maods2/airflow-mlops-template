# Feature Code Module

This directory contains the business logic code for the MLOps framework, including SQL queries, job classes, and the main job orchestrator.

## Directory Structure

```
feature-code/
├── sql/                           # SQL query files
│   ├── ingestion_*.sql          # Ingestion pipeline queries
│   ├── training_*.sql            # Training pipeline queries
│   ├── feature_engineering_*.sql # Feature engineering queries
│   ├── create_raw_data_table.sql # Table creation scripts
│   ├── create_warehouse_table.sql
│   └── create_labels_table.sql
│
├── src/                           # Python source code
│   ├── main.py                   # Job orchestrator with argument parsing
│   ├── predict/                  # Predict job classes
│   │   ├── __init__.py
│   │   └── predict.py
│   ├── preprocess/               # Preprocess job classes
│   │   ├── __init__.py
│   │   └── preprocess.py
│   ├── train/                    # Train job classes
│   │   ├── __init__.py
│   │   └── train.py
│   └── model/                    # Model utilities
│       └── __init__.py
│
└── requirements.txt              # Python dependencies
```

## SQL Files

SQL files use parameter placeholders that are replaced at runtime:
- `{project_id}` - GCP Project ID
- `{dataset_id}` - BigQuery Dataset ID
- `{source_dataset}` - Source dataset name
- `{target_dataset}` - Target dataset name
- `{execution_date}` - Execution date (YYYY-MM-DD)
- `{execution_date_nodash}` - Execution date without dashes (YYYYMMDD)

### Table Creation Scripts

These scripts create the necessary BigQuery tables:

1. **create_raw_data_table.sql** - Creates the raw data table for ingestion
2. **create_warehouse_table.sql** - Creates the warehouse table for processed data
3. **create_labels_table.sql** - Creates the labels table for ML training

## Job Classes

### Predict Job (`predict/predict.py`)

Simulates model prediction/inference jobs. Used for batch inference.

**Usage:**
```bash
python main.py predict \
  --project-id your-project \
  --dataset-id your-dataset \
  --model-path gs://bucket/model \
  --input-table input_table \
  --output-table predictions
```

### Preprocess Job (`preprocess/preprocess.py`)

Simulates data preprocessing and feature engineering.

**Usage:**
```bash
python main.py preprocess \
  --project-id your-project \
  --dataset-id your-dataset \
  --input-table raw_data \
  --output-table preprocessed_data \
  --features feature1 feature2 feature3
```

### Train Job (`train/train.py`)

Simulates model training jobs.

**Usage:**
```bash
python main.py train \
  --project-id your-project \
  --dataset-id your-dataset \
  --input-table training_data \
  --model-path gs://bucket/models/model \
  --model-type xgboost \
  --hyperparameters max_depth=5 learning_rate=0.01 n_estimators=100
```

## Main Job Orchestrator (`main.py`)

The main orchestrator selects and executes jobs based on command-line arguments.

**Features:**
- Argument parsing with argparse
- Configuration validation
- Job execution with proper error handling
- Detailed logging
- Type-safe job configuration

**Arguments:**
- `job_type` - Type of job to execute (predict, preprocess, train)
- `--project-id` - GCP Project ID (required for all jobs)
- `--dataset-id` - BigQuery Dataset ID (required for all jobs)
- Additional job-specific arguments

## Examples

### Running a Predict Job

```bash
cd feature-code/src
python main.py predict \
  --project-id ml-project-123 \
  --dataset-id ml_dataset \
  --model-path gs://ml-bucket/models/latest_model \
  --input-table input_data_20241027 \
  --output-table predictions_20241027
```

### Running a Preprocess Job

```bash
python main.py preprocess \
  --project-id ml-project-123 \
  --dataset-id ml_dataset \
  --input-table raw_data_20241027 \
  --output-table preprocessed_data_20241027 \
  --features age income score rating
```

### Running a Train Job

```bash
python main.py train \
  --project-id ml-project-123 \
  --dataset-id ml_dataset \
  --input-table training_data_20241027 \
  --model-path gs://ml-bucket/models/model_20241027 \
  --model-type xgboost \
  --hyperparameters max_depth=6 learning_rate=0.01 n_estimators=200 subsample=0.8
```

## Integration with Airflow

These job classes are called by Airflow DAGs through Dataproc PySpark operators:

```python
# Example in Airflow DAG
preprocess_task = DataprocSubmitJobOperator(
    task_id="preprocess_data",
    job={
        "pyspark_job": {
            "main_python_file_uri": "gs://bucket/scripts/main.py",
            "args": [
                "preprocess",
                "--project-id", "{{ var.value.gcp_project_id }}",
                "--dataset-id", "{{ var.value.bigquery_dataset_id }}",
                "--input-table", "raw_data_{{ ds_nodash }}",
                "--output-table", "preprocessed_data_{{ ds_nodash }}"
            ]
        }
    }
)
```

## Testing

Test individual jobs:

```bash
# Test predict job
python main.py predict \
  --project-id test-project \
  --dataset-id test_dataset \
  --model-path gs://test-bucket/model \
  --input-table test_input \
  --output-table test_output

# Test preprocess job
python main.py preprocess \
  --project-id test-project \
  --dataset-id test_dataset \
  --input-table test_input \
  --output-table test_output

# Test train job
python main.py train \
  --project-id test-project \
  --dataset-id test_dataset \
  --input-table test_input \
  --model-path gs://test-bucket/model \
  --model-type xgboost
```

## Configuration

Jobs receive configuration through environment variables and command-line arguments:

- **Environment Variables**: Set in Airflow or Docker
- **Command-line Arguments**: Passed from Airflow operators
- **Configuration Dictionary**: Created from parsed arguments

## Error Handling

All jobs include:
- Configuration validation
- Error logging
- Graceful failure handling
- Detailed error messages

## Logging

All jobs use structured logging with:
- Timestamps
- Log levels (INFO, ERROR, WARNING)
- Job-specific context
- Progress indicators

## Future Enhancements

- Add actual ML model implementations
- Add database connection handling
- Add result validation
- Add metrics tracking
- Add caching mechanisms
