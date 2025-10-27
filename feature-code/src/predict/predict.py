"""
Predict Job Class
Real sklearn-based model prediction
"""

import sys
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any
import pickle
from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Predict:
    """Predict job class with real sklearn models"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Predict job
        
        Args:
            config: Configuration dictionary with job parameters
        """
        self.config = config
        self.project_id = config.get('project_id', 'default-project')
        self.dataset_id = config.get('dataset_id', 'default_dataset')
        self.model_path = config.get('model_path', 'gs://bucket/models/model')
        self.input_table = config.get('input_table', 'input_table')
        self.output_table = config.get('output_table', 'predictions')
        
        # Initialize clients
        self.bq_client = bigquery.Client(project=self.project_id)
        self.gcs_client = storage.Client(project=self.project_id)
        
        # Model will be loaded in execute()
        self.model = None
        
    def load_model(self) -> None:
        """Load model from GCS"""
        logger.info(f"Loading model from: {self.model_path}")
        
        # Download from GCS
        bucket_name = self.model_path.split('/')[2]
        blob_path = '/'.join(self.model_path.split('/')[3:])
        
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        model_bytes = blob.download_as_bytes()
        
        # Deserialize model
        self.model = pickle.loads(model_bytes)
        
        logger.info("✓ Model loaded successfully")
    
    def load_data(self) -> pd.DataFrame:
        """Load input data from BigQuery"""
        logger.info(f"Loading input data from: {self.project_id}.{self.dataset_id}.{self.input_table}")
        
        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.{self.input_table}`
        LIMIT 10000
        """
        
        df = self.bq_client.query(query).to_dataframe()
        logger.info(f"Loaded {len(df)} records")
        
        return df
    
    def make_predictions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Make predictions using the loaded model"""
        logger.info("Making predictions...")
        
        # Handle missing values
        df = df.fillna(0)
        
        # Select feature columns (exclude id if present)
        feature_cols = [col for col in df.columns if col not in ['id', 'target_value']]
        X = df[feature_cols]
        
        # Make predictions
        predictions = self.model.predict(X)
        probabilities = None
        
        # Try to get prediction probabilities if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X)
            
        logger.info(f"Made predictions for {len(df)} records")
        
        # Add predictions to dataframe
        df['prediction'] = predictions
        
        # Add probabilities if available
        if probabilities is not None:
            for i in range(probabilities.shape[1]):
                df[f'probability_class_{i}'] = probabilities[:, i]
        
        return df
    
    def save_predictions(self, df: pd.DataFrame) -> None:
        """Save predictions to BigQuery"""
        logger.info(f"Saving predictions to: {self.project_id}.{self.dataset_id}.{self.output_table}")
        
        destination = f"{self.project_id}.{self.dataset_id}.{self.output_table}"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema_update_options=[
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
            ]
        )
        
        job = self.bq_client.load_table_from_dataframe(df, destination, job_config=job_config)
        job.result()
        
        logger.info(f"✓ Predictions saved to {destination}")
    
    def execute(self) -> None:
        """Execute prediction job"""
        logger.info("=" * 60)
        logger.info("PREDICT JOB EXECUTION (Real sklearn)")
        logger.info("=" * 60)
        
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Dataset ID: {self.dataset_id}")
        logger.info(f"Model Path: {self.model_path}")
        logger.info(f"Input Table: {self.input_table}")
        logger.info(f"Output Table: {self.output_table}")
        
        try:
            # Load model
            self.load_model()
            
            # Load input data
            df = self.load_data()
            
            # Make predictions
            df = self.make_predictions(df)
            
            # Save predictions
            self.save_predictions(df)
            
            logger.info("\n✓ Predict job completed successfully!")
            logger.info(f"  - Total records processed: {len(df)}")
            logger.info(f"  - Predictions saved successfully")
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_fields = ['project_id', 'dataset_id', 'input_table', 'output_table', 'model_path']
        missing_fields = [field for field in required_fields if not self.config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required configuration fields: {missing_fields}")
            return False
        
        return True