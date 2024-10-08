from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess

# Define the default arguments for the DAG
default_args = {
    'owner': 'api_call',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_api_call():
    subprocess.run(["python", "/opt/airflow/mediastack_api_call/api_call.py"], check=True)

with DAG(
    'articles_api',
    default_args=default_args,
    schedule_interval='0 8 * * *',  # Run every day at 8:00 AM UTC+2
    catchup=False,
) as dag:
    api_request = PythonOperator(
        task_id='api_request',
        python_callable=run_api_call
    )