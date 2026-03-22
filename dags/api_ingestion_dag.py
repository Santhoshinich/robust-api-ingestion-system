from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# Make your project importable
sys.path.append('/opt/airflow/dags/src')

from ingestion.pipeline_runner import run_pipeline


default_args = {
    "owner": "santhoshini",
    "retries": 2
}


def run_rest_posts():
    run_pipeline(mode="rest", endpoint="posts")


def run_soap_calculator():
    run_pipeline(mode="soap", endpoint="calculator")


with DAG(
    dag_id="api_ingestion_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["portfolio", "ingestion"]
) as dag:

    rest_task = PythonOperator(
        task_id="rest_posts_ingestion",
        python_callable=run_rest_posts
    )

    soap_task = PythonOperator(
        task_id="soap_calculator_ingestion",
        python_callable=run_soap_calculator
    )

    # dependency
    rest_task >> soap_task