"""
Demo 05: Dynamic Task Mapping

Demonstra:
- Dynamic Task Mapping (Airflow 2.3+)
- Processar múltiplos itens dinamicamente
- Expand task mapping

Este exemplo mostra como criar tasks dinamicamente baseado em dados.
"""
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime
from typing import List, Dict


@dag(
    dag_id="demo_05_dynamic_task_mapping",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "tutorial", "dynamic"],
    doc_md=__doc__,
)
def demo_05_dynamic_task_mapping():

    @task
    def get_file_list() -> List[Dict[str, str]]:
        """Simula obtenção de lista de arquivos para processar"""
        print("📋 Obtendo lista de arquivos...")
        files = [
            {"filename": "data_2024-01-01.csv", "size": "100MB"},
            {"filename": "data_2024-01-02.csv", "size": "120MB"},
            {"filename": "data_2024-01-03.csv", "size": "95MB"},
        ]
        print(f"📊 Encontrados {len(files)} arquivos")
        return files

    @task
    def validate_file(file_info: Dict[str, str]) -> Dict[str, str]:
        """Valida cada arquivo individualmente"""
        filename = file_info["filename"]
        print(f"✅ Validando: {filename}")
        file_info["validated"] = True
        file_info["status"] = "valid"
        return file_info

    @task
    def process_file(file_info: Dict[str, str]) -> Dict[str, str]:
        """Processa cada arquivo"""
        filename = file_info["filename"]
        print(f"⚙️ Processando: {filename}")
        file_info["processed"] = True
        return file_info

    @task
    def summarize_results(**context) -> int:
        """Sumariza os resultados"""
        print("📊 Sumarizando resultados...")
        # Em produção, isso agregaria os resultados de todas as tasks
        return 3

    # Obtém lista de arquivos
    files = get_file_list()

    # Valida cada arquivo (dynamic mapping)
    validated = validate_file.expand(file_info=files)

    # Processa cada arquivo validado (dynamic mapping)
    processed = process_file.expand(file_info=validated)

    # Sumariza
    summary = summarize_results()

    files >> validated >> processed >> summary


demo_05_dynamic_task_mapping()

