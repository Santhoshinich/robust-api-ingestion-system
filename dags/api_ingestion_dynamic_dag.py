import os
import sys
import yaml
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

# ---------------------------------------------------
# Fix import paths
# ---------------------------------------------------
sys.path.append("/opt/airflow/dags")

from src.ingestion.pipeline_runner import run_pipeline
from src.utils.alerts import send_slack_alert

# ---------------------------------------------------
# Failure Alert
# ---------------------------------------------------

def slack_fail_alert(context):
    ti = context.get("task_instance")
    dag_id = ti.dag_id
    task_id = ti.task_id
    execution_date = context.get("execution_date")
    exception = context.get("exception")

    log_url = ti.log_url

    message = (
        f"🚨 *Airflow Task Failed*\n"
        f"*DAG:* {dag_id}\n"
        f"*Task:* {task_id}\n"
        f"*Time:* {execution_date}\n"
        f"*Error:* {exception}\n"
        f"*Logs:* <{log_url}|View Logs>"
    )

    SlackWebhookOperator(
        task_id='slack_alert',
        slack_webhook_conn_id='slack_webhook',
        message=message,
    ).execute(context=context)

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
    'on_failure_callback': slack_fail_alert
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
       