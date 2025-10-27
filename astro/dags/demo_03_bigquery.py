"""
Demo 03: Integração com BigQuery

Demonstra:
- BigQueryExecuteQueryOperator
- Executar queries SQL
- Parâmetros e variáveis do Airflow
- Tabelas de destino

Este exemplo mostra integração básica com Google BigQuery.
"""
from airflow.decorators import dag, task
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
)
from pendulum import datetime
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from typing import Dict, Any


@dag(
    dag_id="demo_03_bigquery",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=["demo", "tutorial", "bigquery"],
    doc_md=__doc__,
)
def demo_03_bigquery():

    @task
    def get_execution_date(**context) -> Dict[str, str]:
        """Obtém informações da execução"""
        ds = context["ds"]  # Execution date
        ds_nodash = context["ds_nodash"]  # Execution date without dashes
        print(f"📅 Execution date: {ds}")
        return {"ds": ds, "ds_nodash": ds_nodash}

    @task
    def count_records(**context) -> int:
        """
        Conta registros usando BigQuery
        Nota: Esta é uma versão simplificada.
        Em produção, use BigQueryExecuteQueryOperator
        """
        print("🔍 Contando registros...")
        # Simulando contagem
        count = 100
        print(f"📊 Total de registros: {count}")
        return count

    # Query simples no BigQuery
    create_table = BigQueryExecuteQueryOperator(
        task_id="create_demo_table",
        sql="""
            SELECT 
                'Alice' as name,
                25 as age,
                'Engineer' as job
            UNION ALL
            SELECT 
                'Bob' as name,
                30 as age,
                'Manager' as job
            UNION ALL
            SELECT 
                'Charlie' as name,
                28 as age,
                'Designer' as job
        """,
        destination_dataset_table="{{ var.value.gcp_project_id }}.{{ var.value.bigquery_dataset_id }}.demo_table",
        write_disposition="WRITE_TRUNCATE",
        use_legacy_sql=False,
        gcp_conn_id="google_cloud_default",
    )

    @task
    def show_results(**context):
        """Mostra os resultados da query"""
        print("✅ Tabela criada com sucesso!")
        print("💡 Verifique no BigQuery Console")

    # Define dependências
    execution_info = get_execution_date()
    count = count_records()
    show = show_results()

    execution_info >> count >> create_table >> show


demo_03_bigquery()

