from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

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


with DAG(
    'articles_api',
    default_args=default_args,
    schedule_interval='0 8 * * 1',
    catchup=False,
) as dag:
            api_request = BashOperator(
                    task_id = "api_request",
                    bash_command= "cd /opt/airflow/mediastack_api_call && python api_call.py",
            )