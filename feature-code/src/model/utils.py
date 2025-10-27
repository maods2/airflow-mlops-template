"""
Model Utilities
Helper functions for model training and evaluation
"""

import pandas as pd
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def prepare_data_for_training(df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare data for training
    
    Args:
        df: Input dataframe
        target_column: Name of target column
        
    Returns:
        Tuple of features (X) and target (y)
    """
    if target_column not in df.columns:
        logger.warning(f"Target column {target_column} not found, creating synthetic target")
        y = pd.Series(np.random.randint(0, 2, size=len(df)))
    else:
        y = df[target_column].copy()
    
    # Remove target from features
    X = df.drop(columns=[target_column] if target_column in df.columns else [])
    
    return X, y


def calculate_feature_importance(model, feature_names: list) -> dict:
    """
    Calculate feature importance
    
    Args:
        model: Trained model with feature_importances_ attribute
        feature_names: List of feature names
        
    Returns:
        Dictionary of feature importances
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        importance_dict = dict(zip(feature_names, importances))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_importance)
    else:
        logger.warning("Model does not have feature_importances_ attribute")
        return {}


def save_model_summary(model, feature_names: list, metrics: dict, output_path: str) -> None:
    """
    Save model summary to file
    
    Args:
        model: Trained model
        feature_names: List of feature names
        metrics: Dictionary of evaluation metrics
        output_path: Path to save summary
    """
    with open(output_path, 'w') as f:
        f.write("Model Summary\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("Model Type: " + type(model).__name__ + "\n\n")
        
        f.write("Metrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value:.4f}\n")
        
        f.write("\nFeature Importance:\n")
        importances = calculate_feature_importance(model, feature_names)
        for feature, importance in list(importances.items())[:10]:
            f.write(f"  {feature}: {importance:.4f}\n")


def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Validate data quality
    
    Args:
        df: Input dataframe
        
    Returns:
        Dictionary of quality metrics
    """
    metrics = {
        'total_records': len(df),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_records': df.duplicated().sum(),
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns)
    }
    
    return metrics
