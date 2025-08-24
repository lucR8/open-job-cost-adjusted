from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def ingest_offers():
    from src.pipelines.ingest_offers import run as run_pipeline
    run_pipeline()

default_args = {"owner": "luc", "retries": 2, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="ingest_offers_5min",
    start_date=datetime(2025, 8, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
    default_args=default_args,
    tags=["offers","france-travail"],
) as dag:
    PythonOperator(task_id="ingest_offers", python_callable=ingest_offers)
