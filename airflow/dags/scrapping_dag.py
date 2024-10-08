from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'articles_scrapping',
    default_args=default_args,
    schedule_interval='0 8 * * *',  # Run every day at 8:00 AM UTC+2
    catchup=False,
) as dag:
    scrapping_upcoming = BashOperator(
        task_id = "figaro_articles_scrapper",
        bash_command = 'cd /opt/airflow/article_scrapper && scrapy crawl figarospider',
    )
