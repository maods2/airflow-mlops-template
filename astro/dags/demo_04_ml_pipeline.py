"""
Demo 04: Pipeline de Machine Learning

Demonstra:
- ETL para preparar dados de treino
- Feature Engineering
- Treinamento de modelo (simulado)
- Avaliação de modelo
- Versionamento

Este exemplo simula um pipeline completo de ML end-to-end.
"""
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from pendulum import datetime
from typing import Dict, Any
import json


@dag(
    dag_id="demo_04_ml_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=["demo", "ml", "pipeline", "end-to-end"],
    doc_md=__doc__,
)
def demo_04_ml_pipeline():

    @task
    def extract_raw_data() -> Dict[str, Any]:
        """ETL: Extrai dados brutos"""
        print("📥 ETL: Extraindo dados brutos...")
        # Simulando dados
        return {
            "records": 1000,
            "features": ["age", "income", "score"],
            "date": "2024-01-01"
        }

    @task
    def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """ETL: Limpa e transforma dados"""
        print("🔄 ETL: Processando dados...")
        data["cleaned"] = True
        data["records_after_cleaning"] = 950
        return data

    @task
    def feature_engineering(data: Dict[str, Any]) -> Dict[str, Any]:
        """Feature Engineering: Cria features"""
        print("✨ Feature Engineering: Criando features...")
        data["features"] = [
            "age",
            "income",
            "score",
            "age_normalized",
            "income_log",
            "score_scaled"
        ]
        print(f"✨ Features criadas: {len(data['features'])}")
        return data

    @task
    def split_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Split: Divide em treino e validação"""
        print("✂️ Split: Dividindo dados...")
        return {
            "train_size": 760,
            "val_size": 190,
            "test_size": 95
        }

    @task
    def train_model(**context) -> Dict[str, Any]:
        """
        Training: Treina o modelo
        Em produção, isso executaria em Vertex AI ou Dataproc
        """
        print("🤖 Training: Treinando modelo...")
        # Simulando treinamento
        model_info = {
            "model_id": "model_v1_20240101",
            "algorithm": "XGBoost",
            "params": {
                "max_depth": 6,
                "learning_rate": 0.01,
                "n_estimators": 100
            },
            "metrics": {
                "train_accuracy": 0.95,
                "val_accuracy": 0.92
            }
        }
        print(f"✅ Modelo treinado: {model_info['model_id']}")
        return model_info

    @task
    def evaluate_model(model_info: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluation: Avalia o modelo"""
        print("📊 Evaluation: Avaliando modelo...")
        metrics = model_info["metrics"]
        print(f"📈 Train Accuracy: {metrics['train_accuracy']}")
        print(f"📈 Val Accuracy: {metrics['val_accuracy']}")
        return metrics

    @task
    def register_model(model_info: Dict[str, Any], metrics: Dict[str, Any]):
        """
        Registry: Registra o modelo no Model Registry
        Em produção, isso salvaria no Vertex AI Model Registry
        """
        print("📝 Registry: Registrando modelo...")
        print(f"🤖 Model ID: {model_info['model_id']}")
        print(f"📊 Metrics: {metrics}")
        print("✅ Modelo registrado no Model Registry!")

    @task
    def deploy_model(**context) -> str:
        """Deploy: Faz deploy do modelo"""
        print("🚀 Deploy: Fazendo deploy do modelo...")
        version = "v1.0"
        print(f"✅ Modelo {version} em produção!")
        return version

    # Define o pipeline completo
    raw_data = extract_raw_data()
    cleaned_data = transform_data(raw_data)
    features = feature_engineering(cleaned_data)
    splits = split_data(features)

    # Training phase
    model = train_model()
    metrics = evaluate_model(model)

    # Registry e Deploy
    splits >> model >> metrics
    register_model(model, metrics)
    deployed = deploy_model()
    metrics >> deployed


demo_04_ml_pipeline()

