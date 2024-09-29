from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sqlite3
import requests
import os

# Define the default arguments for the DAG
default_args = {
    'owner': 'data_aggregator',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def aggregate_and_send_data():
    conn = sqlite3.connect('/opt/airflow/airflow.db')
    cursor = conn.cursor()
    
    # Aggregate data from both tables
    cursor.execute('''
    SELECT source, title, content, language
    FROM api_articles
    UNION ALL
    SELECT "Scraping_figaro" as source, title,main_txt as content, "fr" as language
    FROM scraping_articles
    ''')
    
    aggregated_data = cursor.fetchall()
    conn.close()
    
    # Send aggregated data to the database using the db_api
    db_api_url = os.getenv("DB_API_URL")
    db_api_token = os.getenv("DB_API_TOKEN")
    
    for data in aggregated_data:
        article_data = {
            "source": data[0],
            "title": data[1],
            "content": data[2],
            "language": data[3],
        }
        response = requests.post(
            f"{db_api_url}/article/",
            json=article_data,
            headers={"x-token": db_api_token}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to send article to DB: {response.json()}")

with DAG(
    'datasend_dag',
    default_args=default_args,
    schedule_interval='5 8 * * *',  # Run every day at 8:05 AM UTC+2
    catchup=False,
) as dag:
    aggregate_and_send = PythonOperator(
        task_id='aggregate_and_send_data',
        python_callable=aggregate_and_send_data
    )
