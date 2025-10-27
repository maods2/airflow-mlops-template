"""
Main Job Orchestrator
Selects and executes jobs based on command-line arguments
"""

import argparse
import logging
import sys
from typing import Dict, Any

# Import job classes
from predict.predict import Predict
from preprocess.preprocess import Preprocess
from train.train import Train

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='MLOps Job Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run predict job
  python main.py predict --project-id project-123 --dataset-id dataset-1 --model-path gs://bucket/model --input-table input_table --output-table predictions
  
  # Run preprocess job
  python main.py preprocess --project-id project-123 --dataset-id dataset-1 --input-table raw_data --output-table preprocessed_data
  
  # Run train job
  python main.py train --project-id project-123 --dataset-id dataset-1 --input-table training_data --model-path gs://bucket/models/model --model-type xgboost
        """
    )
    
    subparsers = parser.add_subparsers(dest='job_type', help='Job type to execute')
    subparsers.required = True
    
    # Common arguments for all jobs
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--project-id', required=True, help='GCP Project ID')
    common_parser.add_argument('--dataset-id', required=True, help='BigQuery Dataset ID')
    
    # Predict job arguments
    predict_parser = subparsers.add_parser('predict', parents=[common_parser], help='Run predict job')
    predict_parser.add_argument('--model-path', required=True, help='Path to model file')
    predict_parser.add_argument('--input-table', required=True, help='Input table name')
    predict_parser.add_argument('--output-table', required=True, help='Output table name')
    
    # Preprocess job arguments
    preprocess_parser = subparsers.add_parser('preprocess', parents=[common_parser], help='Run preprocess job')
    preprocess_parser.add_argument('--input-table', required=True, help='Input table name')
    preprocess_parser.add_argument('--output-table', required=True, help='Output table name')
    preprocess_parser.add_argument('--features', nargs='+', default=[], help='List of features to use')
    preprocess_parser.add_argument('--bucket-name', default='default-bucket', help='GCS bucket name for artifacts')
    
    # Train job arguments
    train_parser = subparsers.add_parser('train', parents=[common_parser], help='Run train job')
    train_parser.add_argument('--input-table', required=True, help='Input table name')
    train_parser.add_argument('--model-path', required=True, help='Path to save model')
    train_parser.add_argument('--model-type', default='xgboost', help='Type of model to train')
    train_parser.add_argument('--hyperparameters', nargs='+', default=[], help='Hyperparameters as key=value pairs')
    
    return parser.parse_args()


def create_config_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    """Create configuration dictionary from parsed arguments"""
    config = {
        'project_id': args.project_id,
        'dataset_id': args.dataset_id,
    }
    
    if args.job_type == 'predict':
        config.update({
            'model_path': args.model_path,
            'input_table': args.input_table,
            'output_table': args.output_table,
        })
    elif args.job_type == 'preprocess':
        config.update({
            'input_table': args.input_table,
            'output_table': args.output_table,
            'features': args.features,
            'bucket_name': args.bucket_name,
        })
    elif args.job_type == 'train':
        config.update({
            'input_table': args.input_table,
            'model_path': args.model_path,
            'model_type': args.model_type,
            'hyperparameters': parse_hyperparameters(args.hyperparameters),
        })
    
    return config


def parse_hyperparameters(hp_args: list) -> Dict[str, Any]:
    """Parse hyperparameters from command-line arguments"""
    hyperparameters = {}
    for arg in hp_args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            # Try to convert to appropriate type
            try:
                hyperparameters[key] = int(value)
            except ValueError:
                try:
                    hyperparameters[key] = float(value)
                except ValueError:
                    hyperparameters[key] = value
    return hyperparameters


def execute_job(job_type: str, config: Dict[str, Any]) -> None:
    """Execute the specified job type with given configuration"""
    logger.info(f"\n{'='*60}")
    logger.info(f"EXECUTING {job_type.upper()} JOB")
    logger.info(f"{'='*60}\n")
    
    try:
        if job_type == 'predict':
            job = Predict(config)
            if not job.validate_config():
                logger.error("Configuration validation failed")
                sys.exit(1)
            job.execute()
            
        elif job_type == 'preprocess':
            job = Preprocess(config)
            if not job.validate_config():
                logger.error("Configuration validation failed")
                sys.exit(1)
            job.execute()
            
        elif job_type == 'train':
            job = Train(config)
            if not job.validate_config():
                logger.error("Configuration validation failed")
                sys.exit(1)
            job.execute()
            
        else:
            logger.error(f"Unknown job type: {job_type}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error executing job: {e}")
        raise


def main():
    """Main entry point"""
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Create configuration from arguments
        config = create_config_from_args(args)
        
        # Log configuration
        logger.info("Job Configuration:")
        for key, value in config.items():
            logger.info(f"  {key}: {value}")
        
        # Execute the job
        execute_job(args.job_type, config)
        
        logger.info("\n" + "="*60)
        logger.info("JOB EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        
    except KeyboardInterrupt:
        logger.info("\nJob execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
