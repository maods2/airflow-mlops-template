"""
Configuration Loader - Handles loading and validation of YAML configuration files
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError


class ConfigLoader:
    """
    Handles loading and validation of YAML configuration files
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.schema = self._get_config_schema()
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load and validate a configuration file
        
        Args:
            config_file: Name of the configuration file
            
        Returns:
            Validated configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValidationError: If config doesn't match schema
        """
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate configuration
        try:
            validate(instance=config, schema=self.schema)
        except ValidationError as e:
            raise ValidationError(f"Configuration validation failed for {config_file}: {e}")
        
        return config
    
    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all configuration files from the config directory
        
        Returns:
            Dictionary mapping config file names to their configurations
        """
        configs = {}
        config_files = list(self.config_dir.glob("*.yaml"))
        
        for config_file in config_files:
            try:
                configs[config_file.name] = self.load_config(config_file.name)
            except Exception as e:
                print(f"Error loading config {config_file.name}: {e}")
        
        return configs
    
    def _get_config_schema(self) -> Dict[str, Any]:
        """
        Get JSON schema for configuration validation
        
        Returns:
            JSON schema dictionary
        """
        return {
            "type": "object",
            "required": ["dag_name", "type"],
            "properties": {
                "dag_name": {
                    "type": "string",
                    "pattern": "^[a-zA-Z0-9_-]+$"
                },
                "type": {
                    "type": "string",
                    "enum": ["basic", "bigquery", "dataproc", "hybrid"]
                },
                "description": {
                    "type": "string"
                },
                "schedule": {
                    "type": "string"
                },
                "start_date": {
                    "type": "string"
                },
                "default_args": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string"},
                        "retries": {"type": "integer", "minimum": 0},
                        "retry_delay": {"type": "string"},
                        "email": {"type": "array", "items": {"type": "string"}},
                        "email_on_failure": {"type": "boolean"},
                        "email_on_retry": {"type": "boolean"}
                    }
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "project_id": {
                    "type": "string"
                },
                "dataset_id": {
                    "type": "string"
                },
                "region": {
                    "type": "string"
                },
                "cluster_name": {
                    "type": "string"
                },
                "environments": {
                    "type": "object",
                    "properties": {
                        "dev": {
                            "type": "object",
                            "properties": {
                                "project_id": {"type": "string"},
                                "dataset_id": {"type": "string"},
                                "source_dataset": {"type": "string"},
                                "target_dataset": {"type": "string"},
                                "region": {"type": "string"},
                                "cluster_name": {"type": "string"},
                                "bucket_name": {"type": "string"}
                            }
                        },
                        "qa": {
                            "type": "object",
                            "properties": {
                                "project_id": {"type": "string"},
                                "dataset_id": {"type": "string"},
                                "source_dataset": {"type": "string"},
                                "target_dataset": {"type": "string"},
                                "region": {"type": "string"},
                                "cluster_name": {"type": "string"},
                                "bucket_name": {"type": "string"}
                            }
                        },
                        "prod": {
                            "type": "object",
                            "properties": {
                                "project_id": {"type": "string"},
                                "dataset_id": {"type": "string"},
                                "source_dataset": {"type": "string"},
                                "target_dataset": {"type": "string"},
                                "region": {"type": "string"},
                                "cluster_name": {"type": "string"},
                                "bucket_name": {"type": "string"}
                            }
                        }
                    }
                },
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id", "type"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "type": {"type": "string", "enum": ["python", "bash", "sql"]},
                            "python_callable": {"type": "string"},
                            "bash_command": {"type": "string"},
                            "sql_query": {"type": "string"},
                            "depends_on": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "queries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "sql": {"type": "string"},
                            "sql_file": {"type": "string"},
                            "destination_table": {"type": "string"},
                            "write_disposition": {"type": "string", "enum": ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"]},
                            "depends_on": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "jobs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id", "job_type"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "job_type": {"type": "string", "enum": ["pyspark", "spark", "hadoop", "hive", "pig"]},
                            "main_class": {"type": "string"},
                            "main_python_file_uri": {"type": "string"},
                            "jar_file_uris": {"type": "array", "items": {"type": "string"}},
                            "args": {"type": "array", "items": {"type": "string"}},
                            "depends_on": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "bigquery_tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "sql": {"type": "string"},
                            "sql_file": {"type": "string"},
                            "destination_table": {"type": "string"},
                            "write_disposition": {"type": "string", "enum": ["WRITE_TRUNCATE", "WRITE_APPEND", "WRITE_EMPTY"]},
                            "depends_on": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "dataproc_tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["task_id", "job_type"],
                        "properties": {
                            "task_id": {"type": "string"},
                            "job_type": {"type": "string", "enum": ["pyspark", "spark", "hadoop", "hive", "pig"]},
                            "main_class": {"type": "string"},
                            "main_python_file_uri": {"type": "string"},
                            "jar_file_uris": {"type": "array", "items": {"type": "string"}},
                            "args": {"type": "array", "items": {"type": "string"}},
                            "depends_on": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            }
        }
