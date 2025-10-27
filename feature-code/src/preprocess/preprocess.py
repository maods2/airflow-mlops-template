"""
Preprocess Job Class
Real sklearn-based data preprocessing jobs
"""

import sys
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
import pickle
from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Preprocess:
    """Preprocess job class with real sklearn preprocessing"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Preprocess job
        
        Args:
            config: Configuration dictionary with job parameters
        """
        self.config = config
        self.project_id = config.get('project_id', 'default-project')
        self.dataset_id = config.get('dataset_id', 'default_dataset')
        self.input_table = config.get('input_table', 'input_table')
        self.output_table = config.get('output_table', 'preprocessed_data')
        self.features = config.get('features', [])
        
        # Initialize clients
        self.bq_client = bigquery.Client(project=self.project_id)
        self.gcs_client = storage.Client(project=self.project_id)
        
        # Preprocessing objects
        self.imputer = SimpleImputer(strategy='mean')
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load data from BigQuery"""
        logger.info(f"Loading data from: {self.project_id}.{self.dataset_id}.{self.input_table}")
        
        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.{self.input_table}`
        LIMIT 10000
        """
        
        df = self.bq_client.query(query).to_dataframe()
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the data"""
        logger.info("Step 1: Data cleaning...")
        
        initial_count = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        logger.info(f"Removed duplicates: {initial_count - len(df)} records")
        
        # Handle missing values
        df = df.dropna(subset=['id'])
        logger.info(f"Removed records with missing id: {initial_count - len(df)} records")
        
        logger.info(f"Records after cleaning: {len(df)}")
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer new features"""
        logger.info("Step 2: Feature engineering...")
        
        # Create derived features
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['year'] = df['created_at'].dt.year
            df['month'] = df['created_at'].dt.month
            df['day_of_week'] = df['created_at'].dt.dayofweek
            logger.info("Created time-based features: year, month, day_of_week")
        
        # Create interaction features if applicable
        if 'age' in df.columns and 'income' in df.columns:
            df['age_income_interaction'] = df['age'] * df['income']
            logger.info("Created interaction features")
        
        logger.info(f"Total features after engineering: {len(df.columns)}")
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables"""
        logger.info("Step 3: Encoding categorical variables...")
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col not in ['id', 'email']:  # Don't encode IDs and emails
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
                logger.info(f"Encoded column: {col}")
        
        return df
    
    def scale_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scale numerical features"""
        logger.info("Step 4: Feature scaling...")
        
        # Select numerical columns only
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col not in ['id']]
        
        if len(numerical_cols) > 0:
            df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
            logger.info(f"Scaled {len(numerical_cols)} numerical features")
        
        return df
    
    def save_data(self, df: pd.DataFrame) -> None:
        """Save preprocessed data to BigQuery"""
        logger.info(f"Step 5: Saving preprocessed data...")
        
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
        
        logger.info(f"Saved {len(df)} records to {destination}")
    
    def save_preprocessing_artifacts(self) -> None:
        """Save preprocessing artifacts to GCS"""
        logger.info("Saving preprocessing artifacts...")
        
        artifacts = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }
        
        # Save to pickle
        artifact_path = f"gs://{self.config.get('bucket_name', 'default-bucket')}/artifacts/preprocessing_{self.output_table}.pkl"
        
        # Serialize artifacts
        pickle_bytes = pickle.dumps(artifacts)
        
        # Upload to GCS
        bucket_name = artifact_path.split('/')[2]
        blob_path = '/'.join(artifact_path.split('/')[3:])
        
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.upload_from_string(pickle_bytes)
        
        logger.info(f"Saved preprocessing artifacts to {artifact_path}")
        
    def execute(self) -> None:
        """Execute preprocessing job"""
        logger.info("=" * 60)
        logger.info("PREPROCESS JOB EXECUTION (Real sklearn)")
        logger.info("=" * 60)
        
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Dataset ID: {self.dataset_id}")
        logger.info(f"Input Table: {self.input_table}")
        logger.info(f"Output Table: {self.output_table}")
        
        try:
            # Load data
            df = self.load_data()
            
            # Clean data
            df = self.clean_data(df)
            
            # Engineer features
            df = self.engineer_features(df)
            
            # Encode categorical variables
            df = self.encode_categorical(df)
            
            # Scale features
            df = self.scale_features(df)
            
            # Save preprocessed data
            self.save_data(df)
            
            # Save preprocessing artifacts
            self.save_preprocessing_artifacts()
            
            logger.info("\n✓ Preprocess job completed successfully!")
            logger.info(f"  - Input records: {len(df)}")
            logger.info(f"  - Output features: {len(df.columns)}")
            logger.info("  - Preprocessing artifacts saved")
            
        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            raise
        
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_fields = ['project_id', 'dataset_id', 'input_table', 'output_table']
        missing_fields = [field for field in required_fields if not self.config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required configuration fields: {missing_fields}")
            return False
        
        return True