import os
import sys
import yaml
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# ---------------------------------------------------
# Fix import paths
# ---------------------------------------------------
sys.path.append("/opt/airflow/dags")

from src.ingestion.pipeline_runner import run_pipeline
from src.utils.alerts import send_slack_alert

# ---------------------------------------------------
# Failure Alert
# ---------------------------------------------------
def task_failure_alert(context):
    task_instance = context.get("task_instance")

    send_slack_alert(
        message=str(context.get("exception")),
        dag_id=context.get("dag").dag_id,
        task_id=task_instance.task_id,
        log_url=task_instance.log_url
    )

# ---------------------------------------------------
# Load config
# ---------------------------------------------------
CONFIG_PATH = "/opt/airflow/dags/src/config/config.yaml"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

config = load_config()

# ---------------------------------------------------
# Default args (FIXED HERE)
# ---------------------------------------------------
default_args = {
    "owner": "San",
    "retries": 2,
    "on_failure_callback": task_failure_alert  
}

# ---------------------------------------------------
# DAG
# ---------------------------------------------------
with DAG(
    dag_id="api_ingestion_dynamic_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["dynamic", "ingestion", "portfolio"]
) as dag:

    tasks = []

    endpoints = config.get("endpoints", {})

    if not endpoints:
        raise ValueError("No endpoints found in config.yaml")

    for endpoint in endpoints.keys():
        task = PythonOperator(
            task_id=f"rest_{endpoint}",
            python_callable=run_pipeline,
            op_kwargs={
                "mode": "rest",
                "endpoint": endpoint
            }
        )
        tasks.append(task)

    soap_task = PythonOperator(
        task_id="soap_calculator",
        python_callable=run_pipeline,
        op_kwargs={
            "mode": "soap",
            "endpoint": "calculator"
        }
    )

    for t in tasks:
        t >> soap_task
       