"""
DAG Builder - Core functionality for generating DAGs dynamically
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template
from datetime import datetime, timedelta

# Airflow imports (commented out for testing without Airflow)
# from airflow.sdk import dag, task
# from airflow.operators.bash import BashOperator
# from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
# from airflow.providers.google.cloud.operators.dataproc import (
#     DataprocCreateClusterOperator,
#     DataprocSubmitJobOperator,
#     DataprocDeleteClusterOperator
# )
# from airflow.providers.google.cloud.sensors.bigquery import BigQueryJobSensor
# from airflow.sensors.filesystem import FileSensor
# from airflow.models import Variable

from .config_loader import ConfigLoader
from .templates import TemplateManager


class DAGBuilder:
    """
    Main class for building DAGs dynamically from YAML configuration and Jinja2 templates
    """
    
    def __init__(self, config_dir: str = "config", templates_dir: str = "templates", dags_dir: str = "dags", sql_dir: str = "feature-code/sql"):
        self.config_dir = Path(config_dir)
        self.templates_dir = Path(templates_dir)
        self.dags_dir = Path(dags_dir)
        self.sql_dir = Path(sql_dir)
        self.config_loader = ConfigLoader(config_dir)
        self.template_manager = TemplateManager(templates_dir)
        
        # Ensure directories exist
        self.dags_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.sql_dir.mkdir(exist_ok=True)
    
    def build_dag_from_config(self, config_file: str) -> str:
        """
        Build a DAG from a YAML configuration file
        
        Args:
            config_file: Name of the configuration file (e.g., 'ingestion.yaml')
            
        Returns:
            Path to the generated DAG file
        """
        config = self.config_loader.load_config(config_file)
        dag_name = config.get('dag_name', config_file.replace('.yaml', ''))
        
        # Generate DAG content based on configuration
        dag_content = self._generate_dag_content(config)
        
        # Write DAG file
        dag_file_path = self.dags_dir / f"{dag_name}.py"
        with open(dag_file_path, 'w') as f:
            f.write(dag_content)
        
        return str(dag_file_path)
    
    def build_all_dags(self) -> List[str]:
        """
        Build all DAGs from configuration files in the config directory
        
        Returns:
            List of paths to generated DAG files
        """
        generated_dags = []
        config_files = list(self.config_dir.glob("*.yaml"))
        
        for config_file in config_files:
            try:
                dag_path = self.build_dag_from_config(config_file.name)
                generated_dags.append(dag_path)
                print(f"Generated DAG: {dag_path}")
            except Exception as e:
                print(f"Error generating DAG from {config_file.name}: {e}")
        
        return generated_dags
    
    def load_sql_file(self, sql_file: str, environment: str = "prod", execution_date: str = "{{ ds }}", execution_date_nodash: str = "{{ ds_nodash }}") -> str:
        """
        Load SQL file and inject environment parameters
        
        Args:
            sql_file: Name of the SQL file
            environment: Environment name (dev, qa, prod)
            execution_date: Execution date for Airflow macros
            execution_date_nodash: Execution date without dashes
            
        Returns:
            SQL content with parameters injected
        """
        sql_path = self.sql_dir / sql_file
        
        if not sql_path.exists():
            # Try alternative paths
            alternative_paths = [
                Path("feature-code/sql") / sql_file,
                Path("../feature-code/sql") / sql_file,
                Path("sql") / sql_file
            ]
            
            for alt_path in alternative_paths:
                if alt_path.exists():
                    sql_path = alt_path
                    break
            else:
                raise FileNotFoundError(f"SQL file not found: {sql_file}. Tried paths: {[str(p) for p in [sql_path] + alternative_paths]}")
        
        with open(sql_path, 'r') as f:
            sql_content = f.read()
        
        # Get environment variables
        import os
        gcp_project_id = os.getenv('GCP_PROJECT_ID', '{{ var.value.gcp_project_id }}')
        gcp_region = os.getenv('GCP_REGION', '{{ var.value.gcp_region }}')
        gcp_bucket_name = os.getenv('GCP_BUCKET_NAME', f'{gcp_project_id}-ml-bucket')
        gcp_source_dataset = os.getenv('GCP_SOURCE_DATASET', '{{ var.value.bigquery_source_dataset }}')
        gcp_target_dataset = os.getenv('GCP_TARGET_DATASET', '{{ var.value.bigquery_dataset_id }}')
        
        # Default parameters for environment injection
        params = {
            'project_id': gcp_project_id,
            'source_dataset': gcp_source_dataset,
            'target_dataset': gcp_target_dataset,
            'execution_date': execution_date,
            'execution_date_nodash': execution_date_nodash,
            'bucket_name': gcp_bucket_name,
            'region': gcp_region
        }
        
        # Inject parameters into SQL
        for key, value in params.items():
            sql_content = sql_content.replace(f'{{{key}}}', value)
        
        return sql_content
    
    def get_environment_params(self, config: Dict[str, Any], environment: str = "prod") -> Dict[str, str]:
        """
        Get environment-specific parameters from configuration
        
        Args:
            config: Configuration dictionary
            environment: Environment name (dev, qa, prod)
            
        Returns:
            Dictionary of environment parameters
        """
        env_params = config.get('environments', {}).get(environment, {})
        
        # Default to prod values if environment not found
        if not env_params and environment != "prod":
            env_params = config.get('environments', {}).get('prod', {})
        
        return env_params
    
    def _generate_dag_content(self, config: Dict[str, Any]) -> str:
        """
        Generate DAG content based on configuration
        
        Args:
            config: DAG configuration dictionary
            
        Returns:
            Generated DAG Python code as string
        """
        dag_type = config.get('type', 'basic')
        
        if dag_type == 'bigquery':
            return self._generate_bigquery_dag(config)
        elif dag_type == 'dataproc':
            return self._generate_dataproc_dag(config)
        elif dag_type == 'hybrid':
            return self._generate_hybrid_dag(config)
        else:
            return self._generate_basic_dag(config)
    
    def _generate_basic_dag(self, config: Dict[str, Any]) -> str:
        """Generate a basic DAG with Python tasks"""
        template = self.template_manager.get_template('basic_dag.py.j2')
        
        return template.render(
            dag_name=config.get('dag_name', 'basic_dag'),
            description=config.get('description', 'Basic DAG'),
            schedule=config.get('schedule', '@daily'),
            start_date=config.get('start_date', 'datetime(2024, 1, 1)'),
            tasks=config.get('tasks', []),
            default_args=config.get('default_args', {}),
            tags=config.get('tags', [])
        )
    
    def _generate_bigquery_dag(self, config: Dict[str, Any]) -> str:
        """Generate a DAG for BigQuery operations"""
        template = self.template_manager.get_template('bigquery_dag.py.j2')
        
        # Get environment variables
        import os
        gcp_project_id = os.getenv('GCP_PROJECT_ID', '{{ var.value.gcp_project_id }}')
        gcp_target_dataset = os.getenv('GCP_TARGET_DATASET', '{{ var.value.bigquery_dataset_id }}')
        
        # Process queries to load SQL from files
        processed_queries = []
        for query in config.get('queries', []):
            processed_query = query.copy()
            if 'sql_file' in query:
                # Load SQL from file and inject parameters
                sql_content = self.load_sql_file(query['sql_file'])
                processed_query['sql'] = sql_content
            processed_queries.append(processed_query)
        
        return template.render(
            dag_name=config.get('dag_name', 'bigquery_dag'),
            description=config.get('description', 'BigQuery DAG'),
            schedule=config.get('schedule', '@daily'),
            start_date=config.get('start_date', 'datetime(2024, 1, 1)'),
            project_id=gcp_project_id,
            dataset_id=gcp_target_dataset,
            queries=processed_queries,
            default_args=config.get('default_args', {}),
            tags=config.get('tags', [])
        )
    
    def _generate_dataproc_dag(self, config: Dict[str, Any]) -> str:
        """Generate a DAG for Dataproc operations"""
        template = self.template_manager.get_template('dataproc_dag.py.j2')
        
        # Get environment variables
        import os
        gcp_project_id = os.getenv('GCP_PROJECT_ID', '{{ var.value.gcp_project_id }}')
        gcp_region = os.getenv('GCP_REGION', '{{ var.value.gcp_region }}')
        gcp_bucket_name = os.getenv('GCP_BUCKET_NAME', f'{gcp_project_id}-ml-bucket')
        
        return template.render(
            dag_name=config.get('dag_name', 'dataproc_dag'),
            description=config.get('description', 'Dataproc DAG'),
            schedule=config.get('schedule', '@daily'),
            start_date=config.get('start_date', 'datetime(2024, 1, 1)'),
            project_id=gcp_project_id,
            region=gcp_region,
            cluster_name=config.get('cluster_name', '{{ dag.dag_id }}-cluster'),
            bucket_name=gcp_bucket_name,
            jobs=config.get('jobs', []),
            default_args=config.get('default_args', {}),
            tags=config.get('tags', [])
        )
    
    def _generate_hybrid_dag(self, config: Dict[str, Any]) -> str:
        """Generate a hybrid DAG with both BigQuery and Dataproc operations"""
        template = self.template_manager.get_template('hybrid_dag.py.j2')
        
        # Get environment variables
        import os
        gcp_project_id = os.getenv('GCP_PROJECT_ID', '{{ var.value.gcp_project_id }}')
        gcp_region = os.getenv('GCP_REGION', '{{ var.value.gcp_region }}')
        gcp_bucket_name = os.getenv('GCP_BUCKET_NAME', f'{gcp_project_id}-ml-bucket')
        gcp_target_dataset = os.getenv('GCP_TARGET_DATASET', '{{ var.value.bigquery_dataset_id }}')
        
        # Process BigQuery tasks to load SQL from files
        processed_bigquery_tasks = []
        for task in config.get('bigquery_tasks', []):
            processed_task = task.copy()
            if 'sql_file' in task:
                # Load SQL from file and inject parameters
                sql_content = self.load_sql_file(task['sql_file'])
                processed_task['sql'] = sql_content
            processed_bigquery_tasks.append(processed_task)
        
        return template.render(
            dag_name=config.get('dag_name', 'hybrid_dag'),
            description=config.get('description', 'Hybrid DAG'),
            schedule=config.get('schedule', '@daily'),
            start_date=config.get('start_date', 'datetime(2024, 1, 1)'),
            project_id=gcp_project_id,
            dataset_id=gcp_target_dataset,
            region=gcp_region,
            cluster_name=config.get('cluster_name', '{{ dag.dag_id }}-cluster'),
            bucket_name=gcp_bucket_name,
            bigquery_tasks=processed_bigquery_tasks,
            dataproc_tasks=config.get('dataproc_tasks', []),
            default_args=config.get('default_args', {}),
            tags=config.get('tags', [])
        )
    
    def cleanup_old_dags(self, keep_files: List[str] = None):
        """
        Clean up old DAG files, keeping specified files
        
        Args:
            keep_files: List of files to keep (e.g., ['__init__.py', 'exampledag.py'])
        """
        if keep_files is None:
            keep_files = ['__init__.py', 'exampledag.py']
        
        for dag_file in self.dags_dir.glob("*.py"):
            if dag_file.name not in keep_files:
                try:
                    dag_file.unlink()
                    print(f"Removed old DAG: {dag_file}")
                except Exception as e:
                    print(f"Error removing {dag_file}: {e}")
