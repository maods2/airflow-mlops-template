"""
Train Job Class
Real sklearn-based model training
"""

import sys
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
from google.cloud import bigquery
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Train:
    """Train job class with real sklearn models"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Train job
        
        Args:
            config: Configuration dictionary with job parameters
        """
        self.config = config
        self.project_id = config.get('project_id', 'default-project')
        self.dataset_id = config.get('dataset_id', 'default_dataset')
        self.input_table = config.get('input_table', 'training_data')
        self.model_path = config.get('model_path', 'gs://bucket/models/model')
        self.model_type = config.get('model_type', 'random_forest').lower()
        self.hyperparameters = config.get('hyperparameters', {})
        
        # Initialize clients
        self.bq_client = bigquery.Client(project=self.project_id)
        self.gcs_client = storage.Client(project=self.project_id)
        
        # Initialize model
        self.model = self._create_model()
        
    def _create_model(self):
        """Create model based on type"""
        logger.info(f"Creating {self.model_type} model...")
        
        if self.model_type == 'random_forest':
            n_estimators = self.hyperparameters.get('n_estimators', 100)
            max_depth = self.hyperparameters.get('max_depth', 10)
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=42
            )
        elif self.model_type == 'gradient_boosting' or self.model_type == 'xgboost':
            n_estimators = self.hyperparameters.get('n_estimators', 100)
            learning_rate = self.hyperparameters.get('learning_rate', 0.01)
            max_depth = self.hyperparameters.get('max_depth', 5)
            model = GradientBoostingClassifier(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
                random_state=42
            )
        elif self.model_type == 'logistic_regression':
            C = self.hyperparameters.get('C', 1.0)
            model = LogisticRegression(C=C, random_state=42, max_iter=1000)
        else:
            logger.warning(f"Unknown model type {self.model_type}, using RandomForest")
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        return model
    
    def load_data(self) -> tuple:
        """Load and split data from BigQuery"""
        logger.info(f"Loading data from: {self.project_id}.{self.dataset_id}.{self.input_table}")
        
        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.{self.input_table}`
        """
        
        df = self.bq_client.query(query).to_dataframe()
        logger.info(f"Loaded {len(df)} records")
        
        # Separate features and target
        if 'target_value' in df.columns:
            X = df.drop('target_value', axis=1)
            y = df['target_value']
            
            # Convert to binary classification if needed
            if y.dtype == float and y.nunique() > 2:
                y = (y > y.median()).astype(int)
        else:
            logger.warning("No target_value column found, creating synthetic target")
            X = df
            y = np.random.randint(0, 2, size=len(df))
        
        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target shape: {y.shape}")
        
        return X, y
    
    def split_data(self, X: pd.DataFrame, y: pd.Series) -> tuple:
        """Split data into train, validation, and test sets"""
        logger.info("Splitting data...")
        
        # First split: train + val vs test (70% train+val, 30% test)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Second split: train vs val (70% train, 15% val)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=0.214, random_state=42, stratify=y_temp  # 0.214 ~= 15%/70%
        )
        
        logger.info(f"  - Training set: {len(X_train)} samples")
        logger.info(f"  - Validation set: {len(X_val)} samples")
        logger.info(f"  - Test set: {len(X_test)} samples")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Train the model"""
        logger.info(f"Training {self.model_type} model...")
        
        # Handle missing values
        X_train = X_train.fillna(0)
        
        self.model.fit(X_train, y_train)
        
        logger.info("✓ Model training completed")
    
    def evaluate_model(self, X_train: pd.DataFrame, X_val: pd.DataFrame, X_test: pd.DataFrame,
                      y_train: pd.Series, y_val: pd.Series, y_test: pd.Series) -> Dict[str, float]:
        """Evaluate the model"""
        logger.info("Evaluating model...")
        
        # Handle missing values
        X_train = X_train.fillna(0)
        X_val = X_val.fillna(0)
        X_test = X_test.fillna(0)
        
        # Make predictions
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'train_accuracy': accuracy_score(y_train, train_pred),
            'val_accuracy': accuracy_score(y_val, val_pred),
            'test_accuracy': accuracy_score(y_test, test_pred),
            'train_precision': precision_score(y_train, train_pred, zero_division=0),
            'train_recall': recall_score(y_train, train_pred, zero_division=0),
            'train_f1': f1_score(y_train, train_pred, zero_division=0),
            'val_precision': precision_score(y_val, val_pred, zero_division=0),
            'val_recall': recall_score(y_val, val_pred, zero_division=0),
            'val_f1': f1_score(y_val, val_pred, zero_division=0),
            'test_precision': precision_score(y_test, test_pred, zero_division=0),
            'test_recall': recall_score(y_test, test_pred, zero_division=0),
            'test_f1': f1_score(y_test, test_pred, zero_division=0),
        }
        
        logger.info(f"  - Training Accuracy: {metrics['train_accuracy']:.4f}")
        logger.info(f"  - Validation Accuracy: {metrics['val_accuracy']:.4f}")
        logger.info(f"  - Test Accuracy: {metrics['test_accuracy']:.4f}")
        logger.info(f"  - Test Precision: {metrics['test_precision']:.4f}")
        logger.info(f"  - Test Recall: {metrics['test_recall']:.4f}")
        logger.info(f"  - Test F1-Score: {metrics['test_f1']:.4f}")
        
        return metrics
    
    def save_model(self) -> None:
        """Save model to GCS"""
        logger.info(f"Saving model to: {self.model_path}")
        
        # Serialize model
        model_bytes = pickle.dumps(self.model)
        
        # Upload to GCS
        bucket_name = self.model_path.split('/')[2]
        blob_path = '/'.join(self.model_path.split('/')[3:])
        
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.upload_from_string(model_bytes)
        
        logger.info("✓ Model saved successfully")
    
    def save_metrics(self, metrics: Dict[str, float]) -> None:
        """Save metrics to BigQuery"""
        logger.info("Saving metrics to BigQuery...")
        
        # Create metrics table
        metrics_table = f"{self.project_id}.{self.dataset_id}.model_metrics"
        
        metrics_df = pd.DataFrame([metrics])
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        
        job = self.bq_client.load_table_from_dataframe(metrics_df, metrics_table, job_config=job_config)
        job.result()
        
        logger.info("✓ Metrics saved successfully")
        
    def execute(self) -> None:
        """Execute training job"""
        logger.info("=" * 60)
        logger.info("TRAIN JOB EXECUTION (Real sklearn)")
        logger.info("=" * 60)
        
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Dataset ID: {self.dataset_id}")
        logger.info(f"Model Type: {self.model_type}")
        logger.info(f"Hyperparameters: {self.hyperparameters}")
        
        try:
            # Load data
            X, y = self.load_data()
            
            # Split data
            X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(X, y)
            
            # Train model
            self.train_model(X_train, y_train)
            
            # Evaluate model
            metrics = self.evaluate_model(X_train, X_val, X_test, y_train, y_val, y_test)
            
            # Save model
            self.save_model()
            
            # Save metrics
            self.save_metrics(metrics)
            
            logger.info("\n✓ Train job completed successfully!")
            logger.info(f"  - Final accuracy: {metrics['test_accuracy']:.4f}")
            logger.info(f"  - Model saved to: {self.model_path}")
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            raise
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        required_fields = ['project_id', 'dataset_id', 'input_table', 'model_path']
        missing_fields = [field for field in required_fields if not self.config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required configuration fields: {missing_fields}")
            return False
        
        return True