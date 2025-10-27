"""
Demo 01: DAG Simples com Python Operators

Demonstra:
- TaskFlow API
- Python Operators básicos
- XCom para compartilhar dados entre tasks
- Dependências simples

Este é o exemplo mais simples possível de um DAG Airflow.
"""
from airflow.decorators import dag, task
from pendulum import datetime
from typing import Any, Dict


@dag(
    dag_id="demo_01_simple_python",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=["demo", "tutorial", "simple"],
    doc_md=__doc__,
)
def demo_01_simple_python():

    @task
    def extract_data() -> Dict[str, Any]:
        """Extract: Simula extração de dados de uma API"""
        print("📥 Extract: Buscando dados da API...")
        return {
            "users": 100,
            "products": 50,
            "timestamp": "2024-01-01T10:00:00"
        }

    @task
    def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform: Processa e transforma os dados"""
        print(f"🔄 Transform: Processando {data['users']} usuários...")
        data["total_records"] = data["users"] + data["products"]
        data["processed"] = True
        return data

    @task
    def load_data(data: Dict[str, Any]) -> None:
        """Load: Salva os dados processados"""
        print(f"💾 Load: Salvando {data['total_records']} registros...")
        print(f"📊 Dados finais: {data}")

    # Define o fluxo: extract -> transform -> load
    extracted = extract_data()
    transformed = transform_data(extracted)
    load_data(transformed)


# Instancia o DAG
demo_01_simple_python()

