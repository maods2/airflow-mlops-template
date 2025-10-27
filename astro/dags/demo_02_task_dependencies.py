"""
Demo 02: Dependências Complexas entre Tasks

Demonstra:
- Múltiplas dependências
- Paralelismo (tasks que rodam em paralelo)
- Join de dependências
- Conditional branches

Este exemplo mostra como controlar o fluxo de execução de um pipeline.
"""
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime
from typing import List


@dag(
    dag_id="demo_02_task_dependencies",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "tutorial", "dependencies"],
    doc_md=__doc__,
)
def demo_02_task_dependencies():

    # Task inicial: source de dados
    start = BashOperator(
        task_id="start",
        bash_command='echo "🚀 Pipeline iniciado!"',
    )

    @task
    def extract_user_data():
        """Extrai dados de usuários"""
        print("📊 Extraindo dados de usuários...")
        return ["user1", "user2", "user3"]

    @task
    def extract_product_data():
        """Extrai dados de produtos - roda em paralelo"""
        print("📊 Extraindo dados de produtos...")
        return ["product1", "product2"]

    @task
    def validate_data(data: List[str]) -> bool:
        """Valida se os dados estão completos"""
        is_valid = len(data) > 0
        print(f"✅ Validação: {is_valid}")
        return is_valid

    @task
    def process_users(users: List[str]):
        """Processa dados de usuários"""
        print(f"👥 Processando {len(users)} usuários...")

    @task
    def process_products(products: List[str]):
        """Processa dados de produtos"""
        print(f"🛍️ Processando {len(products)} produtos...")

    @task
    def send_notification():
        """Notifica que o pipeline terminou"""
        print("📧 Enviando notificação de conclusão!")

    # Task final
    end = BashOperator(
        task_id="end",
        bash_command='echo "✅ Pipeline concluído!"',
    )

    # Extrações em paralelo
    users = extract_user_data()
    products = extract_product_data()

    # Validação de cada conjunto
    validate_users = validate_data(users)
    validate_products = validate_data(products)

    # Processamento (depende da validação)
    processed_users = process_users(users)
    processed_products = process_products(products)

    # Join: ambas as validações devem passar
    # Avisar finalização
    notification = send_notification()

    # Define dependências:
    # start -> [users, products] -> [validate_users, validate_products] ->
    # [process_users, process_products] -> notification -> end
    start >> [users, products]
    users >> validate_users >> processed_users
    products >> validate_products >> processed_products
    [processed_users, processed_products] >> notification >> end


demo_02_task_dependencies()

