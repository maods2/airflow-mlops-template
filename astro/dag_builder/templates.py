"""
Template Manager - Handles Jinja2 templates for DAG generation
"""

import os
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape


class TemplateManager:
    """
    Manages Jinja2 templates for DAG generation
    """
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['snake_case'] = self._snake_case
        self.env.filters['camel_case'] = self._camel_case
    
    def get_template(self, template_name: str) -> Template:
        """
        Get a Jinja2 template by name
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Jinja2 Template object
        """
        return self.env.get_template(template_name)
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render a template with given context
        
        Args:
            template_name: Name of the template file
            **kwargs: Context variables for template rendering
            
        Returns:
            Rendered template as string
        """
        template = self.get_template(template_name)
        return template.render(**kwargs)
    
    def create_default_templates(self):
        """Create default Jinja2 templates if they don't exist"""
        self._create_basic_dag_template()
        self._create_bigquery_dag_template()
        self._create_dataproc_dag_template()
        self._create_hybrid_dag_template()
        self._create_sql_query_template()
        self._create_python_script_template()
    
    def _create_basic_dag_template(self):
        """Create basic DAG template"""
        template_content = '''"""
{{ description }}

Generated DAG: {{ dag_name }}
"""

from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime
from typing import Any, Dict

# Default arguments
default_args = {
    "owner": "{{ default_args.owner | default('airflow') }}",
    "retries": {{ default_args.retries | default(1) }},
    "retry_delay": "{{ default_args.retry_delay | default('00:05:00') }}",
    "email": {{ default_args.email | default([]) }},
    "email_on_failure": {{ default_args.email_on_failure | default(false) }},
    "email_on_retry": {{ default_args.email_on_retry | default(false) }}
}

@dag(
    dag_id="{{ dag_name }}",
    start_date=datetime({{ start_date | default('2024, 1, 1') }}),
    schedule="{{ schedule | default('@daily') }}",
    default_args=default_args,
    description="{{ description | default('Basic DAG') }}",
    tags={{ tags | default([]) }},
    catchup=False,
    max_active_runs=1
)
def {{ dag_name | snake_case }}():
    {% for task in tasks %}
    {% if task.type == 'python' %}
    @task(task_id="{{ task.task_id }}")
    def {{ task.task_id | snake_case }}(**context) -> Any:
        """
        {{ task.description | default('Python task') }}
        """
        # Import your Python function here
        # from feature_code.src.main import your_function
        # return your_function()
        pass
    
    {% elif task.type == 'bash' %}
    {{ task.task_id | snake_case }} = BashOperator(
        task_id="{{ task.task_id }}",
        bash_command="{{ task.bash_command }}",
        {% if task.depends_on %}
        depends_on_past=False,
        {% endif %}
    )
    {% elif task.type == 'sql' %}
    {{ task.task_id | snake_case }} = BashOperator(
        task_id="{{ task.task_id }}",
        bash_command="echo 'SQL task: {{ task.sql_query }}'",
        {% if task.depends_on %}
        depends_on_past=False,
        {% endif %}
    )
    {% endif %}
    {% endfor %}
    
    # Define task dependencies
    {% for task in tasks %}
    {% if task.depends_on %}
    {% for dep in task.depends_on %}
    {{ task.task_id | snake_case }} >> {{ dep | snake_case }}
    {% endfor %}
    {% endif %}
    {% endfor %}

# Instantiate the DAG
{{ dag_name | snake_case }}()
'''
        
        template_path = self.templates_dir / "basic_dag.py.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _create_bigquery_dag_template(self):
        """Create BigQuery DAG template"""
        template_content = '''"""
{{ description }}

Generated BigQuery DAG: {{ dag_name }}
"""

from airflow.sdk import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.sensors.bigquery import BigQueryJobSensor
from pendulum import datetime
from typing import Any, Dict

# Default arguments
default_args = {
    "owner": "{{ default_args.owner | default('airflow') }}",
    "retries": {{ default_args.retries | default(1) }},
    "retry_delay": "{{ default_args.retry_delay | default('00:05:00') }}",
    "email": {{ default_args.email | default([]) }},
    "email_on_failure": {{ default_args.email_on_failure | default(false) }},
    "email_on_retry": {{ default_args.email_on_retry | default(false) }}
}

@dag(
    dag_id="{{ dag_name }}",
    start_date=datetime({{ start_date | default('2024, 1, 1') }}),
    schedule="{{ schedule | default('@daily') }}",
    default_args=default_args,
    description="{{ description | default('BigQuery DAG') }}",
    tags={{ tags | default([]) }},
    catchup=False,
    max_active_runs=1
)
def {{ dag_name | snake_case }}():
    {% for query in queries %}
    {{ query.task_id | snake_case }} = BigQueryExecuteQueryOperator(
        task_id="{{ query.task_id }}",
        sql="{{ query.sql }}",
        {% if query.destination_table %}
        destination_dataset_table="{{ project_id }}.{{ dataset_id }}.{{ query.destination_table }}",
        {% endif %}
        {% if query.write_disposition %}
        write_disposition="{{ query.write_disposition }}",
        {% endif %}
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default"
    )
    {% endfor %}
    
    # Define task dependencies
    {% for query in queries %}
    {% if query.depends_on %}
    {% for dep in query.depends_on %}
    {{ query.task_id | snake_case }} >> {{ dep | snake_case }}
    {% endfor %}
    {% endif %}
    {% endfor %}

# Instantiate the DAG
{{ dag_name | snake_case }}()
'''
        
        template_path = self.templates_dir / "bigquery_dag.py.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _create_dataproc_dag_template(self):
        """Create Dataproc DAG template"""
        template_content = '''"""
{{ description }}

Generated Dataproc DAG: {{ dag_name }}
"""

from airflow.sdk import dag, task
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocSubmitJobOperator,
    DataprocDeleteClusterOperator
)
from pendulum import datetime
from typing import Any, Dict

# Default arguments
default_args = {
    "owner": "{{ default_args.owner | default('airflow') }}",
    "retries": {{ default_args.retries | default(1) }},
    "retry_delay": "{{ default_args.retry_delay | default('00:05:00') }}",
    "email": {{ default_args.email | default([]) }},
    "email_on_failure": {{ default_args.email_on_failure | default(false) }},
    "email_on_retry": {{ default_args.email_on_retry | default(false) }}
}

@dag(
    dag_id="{{ dag_name }}",
    start_date=datetime({{ start_date | default('2024, 1, 1') }}),
    schedule="{{ schedule | default('@daily') }}",
    default_args=default_args,
    description="{{ description | default('Dataproc DAG') }}",
    tags={{ tags | default([]) }},
    catchup=False,
    max_active_runs=1
)
def {{ dag_name | snake_case }}():
    # Create cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ project_id }}",
        cluster_config={
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n1-standard-2",
                "disk_config": {
                    "boot_disk_type": "pd-standard",
                    "boot_disk_size_gb": 100
                }
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n1-standard-2",
                "disk_config": {
                    "boot_disk_type": "pd-standard",
                    "boot_disk_size_gb": 100
                }
            }
        },
        region="{{ region }}",
        cluster_name="{{ cluster_name }}",
        gcp_conn_id="google_cloud_default"
    )
    
    {% for job in jobs %}
    {{ job.task_id | snake_case }} = DataprocSubmitJobOperator(
        task_id="{{ job.task_id }}",
        project_id="{{ project_id }}",
        job={
            "reference": {"job_id": "{{ job.task_id }}-{{ ts_nodash }}"},
            "placement": {"cluster_name": "{{ cluster_name }}"},
            "{{ job.job_type }}_job": {
                {% if job.job_type == 'pyspark' %}
                "main_python_file_uri": "{{ job.main_python_file_uri }}",
                {% elif job.job_type == 'spark' %}
                "main_class": "{{ job.main_class }}",
                "jar_file_uris": {{ job.jar_file_uris | default([]) }},
                {% endif %}
                "args": {{ job.args | default([]) }}
            }
        },
        region="{{ region }}",
        gcp_conn_id="google_cloud_default"
    )
    {% endfor %}
    
    # Delete cluster
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ project_id }}",
        cluster_name="{{ cluster_name }}",
        region="{{ region }}",
        gcp_conn_id="google_cloud_default",
        trigger_rule="all_done"
    )
    
    # Define task dependencies
    create_cluster >> [
        {% for job in jobs %}
        {{ job.task_id | snake_case }}{% if not loop.last %},{% endif %}
        {% endfor %}
    ] >> delete_cluster
    
    {% for job in jobs %}
    {% if job.depends_on %}
    {% for dep in job.depends_on %}
    {{ dep | snake_case }} >> {{ job.task_id | snake_case }}
    {% endfor %}
    {% endif %}
    {% endfor %}

# Instantiate the DAG
{{ dag_name | snake_case }}()
'''
        
        template_path = self.templates_dir / "dataproc_dag.py.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _create_hybrid_dag_template(self):
        """Create hybrid DAG template"""
        template_content = '''"""
{{ description }}

Generated Hybrid DAG: {{ dag_name }}
"""

from airflow.sdk import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocSubmitJobOperator,
    DataprocDeleteClusterOperator
)
from pendulum import datetime
from typing import Any, Dict

# Default arguments
default_args = {
    "owner": "{{ default_args.owner | default('airflow') }}",
    "retries": {{ default_args.retries | default(1) }},
    "retry_delay": "{{ default_args.retry_delay | default('00:05:00') }}",
    "email": {{ default_args.email | default([]) }},
    "email_on_failure": {{ default_args.email_on_failure | default(false) }},
    "email_on_retry": {{ default_args.email_on_retry | default(false) }}
}

@dag(
    dag_id="{{ dag_name }}",
    start_date=datetime({{ start_date | default('2024, 1, 1') }}),
    schedule="{{ schedule | default('@daily') }}",
    default_args=default_args,
    description="{{ description | default('Hybrid DAG') }}",
    tags={{ tags | default([]) }},
    catchup=False,
    max_active_runs=1
)
def {{ dag_name | snake_case }}():
    # BigQuery tasks
    {% for task in bigquery_tasks %}
    {{ task.task_id | snake_case }} = BigQueryExecuteQueryOperator(
        task_id="{{ task.task_id }}",
        sql="{{ task.sql }}",
        {% if task.destination_table %}
        destination_dataset_table="{{ project_id }}.{{ dataset_id }}.{{ task.destination_table }}",
        {% endif %}
        {% if task.write_disposition %}
        write_disposition="{{ task.write_disposition }}",
        {% endif %}
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default"
    )
    {% endfor %}
    
    # Create Dataproc cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ project_id }}",
        cluster_config={
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n1-standard-2",
                "disk_config": {
                    "boot_disk_type": "pd-standard",
                    "boot_disk_size_gb": 100
                }
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n1-standard-2",
                "disk_config": {
                    "boot_disk_type": "pd-standard",
                    "boot_disk_size_gb": 100
                }
            }
        },
        region="{{ region }}",
        cluster_name="{{ cluster_name }}",
        gcp_conn_id="google_cloud_default"
    )
    
    # Dataproc tasks
    {% for task in dataproc_tasks %}
    {{ task.task_id | snake_case }} = DataprocSubmitJobOperator(
        task_id="{{ task.task_id }}",
        project_id="{{ project_id }}",
        job={
            "reference": {"job_id": "{{ task.task_id }}-{{ ts_nodash }}"},
            "placement": {"cluster_name": "{{ cluster_name }}"},
            "{{ task.job_type }}_job": {
                {% if task.job_type == 'pyspark' %}
                "main_python_file_uri": "{{ task.main_python_file_uri }}",
                {% elif task.job_type == 'spark' %}
                "main_class": "{{ task.main_class }}",
                "jar_file_uris": {{ task.jar_file_uris | default([]) }},
                {% endif %}
                "args": {{ task.args | default([]) }}
            }
        },
        region="{{ region }}",
        gcp_conn_id="google_cloud_default"
    )
    {% endfor %}
    
    # Delete cluster
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ project_id }}",
        cluster_name="{{ cluster_name }}",
        region="{{ region }}",
        gcp_conn_id="google_cloud_default",
        trigger_rule="all_done"
    )
    
    # Define task dependencies
    {% if bigquery_tasks and dataproc_tasks %}
    # BigQuery tasks run first, then Dataproc
    {% for task in bigquery_tasks %}
    {% if task.depends_on %}
    {% for dep in task.depends_on %}
    {{ dep | snake_case }} >> {{ task.task_id | snake_case }}
    {% endfor %}
    {% endif %}
    {% endfor %}
    
    # All BigQuery tasks complete before Dataproc
    [{% for task in bigquery_tasks %}{{ task.task_id | snake_case }}{% if not loop.last %}, {% endif %}{% endfor %}] >> create_cluster
    
    create_cluster >> [
        {% for task in dataproc_tasks %}
        {{ task.task_id | snake_case }}{% if not loop.last %},{% endif %}
        {% endfor %}
    ] >> delete_cluster
    {% endif %}

# Instantiate the DAG
{{ dag_name | snake_case }}()
'''
        
        template_path = self.templates_dir / "hybrid_dag.py.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _create_sql_query_template(self):
        """Create SQL query template"""
        template_content = '''-- {{ description }}
-- Generated SQL query for {{ dag_name }}

{% for query in queries %}
-- {{ query.description | default('SQL Query') }}
{{ query.sql }}

{% endfor %}
'''
        
        template_path = self.templates_dir / "sql_query.sql.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _create_python_script_template(self):
        """Create Python script template"""
        template_content = '''"""
{{ description }}
Generated Python script for {{ dag_name }}
"""

import sys
import os
from pathlib import Path

# Add feature-code to path
feature_code_path = Path(__file__).parent.parent.parent / "feature-code" / "src"
sys.path.append(str(feature_code_path))

{% for task in tasks %}
{% if task.type == 'python' %}
def {{ task.task_id | snake_case }}():
    """
    {{ task.description | default('Python task') }}
    """
    # Import your function from feature-code
    # from main import your_function
    # return your_function()
    pass

{% endif %}
{% endfor %}

if __name__ == "__main__":
    # Execute tasks
    {% for task in tasks %}
    {% if task.type == 'python' %}
    {{ task.task_id | snake_case }}()
    {% endif %}
    {% endfor %}
'''
        
        template_path = self.templates_dir / "python_script.py.j2"
        if not template_path.exists():
            with open(template_path, 'w') as f:
                f.write(template_content)
    
    def _snake_case(self, text: str) -> str:
        """Convert text to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _camel_case(self, text: str) -> str:
        """Convert text to camelCase"""
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
