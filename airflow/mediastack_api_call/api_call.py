import requests
import os
import logging
import sqlite3

def insert_article_to_sqlite(article):
    conn = sqlite3.connect('/opt/airflow/airflow.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        content TEXT,
        language TEXT
    )
    ''')
    
    # Insert data
    cursor.execute('''
    INSERT INTO api_articles (source, title, content, language) 
    VALUES (?, ?, ?, ?)
    ''', (f"Mediastack_{article['source']}", article.get('title', ''), article.get('description', ''), article.get('language', '')))
    
    conn.commit()
    conn.close()

api_key = '23bad5487cd57f506aeb4f15abd709f8'
params = {
    'access_key': api_key,
    'languages': 'fr,en,de,it,pt,hi,es',  # Fetch news in llm's supported languages
    'limit': 10,  # Limit the results to 10 articles
}

# Mediastack API endpoint for fetching news
url = 'http://api.mediastack.com/v1/news'

# Make the API request
response = requests.get(url, params=params)

print(response.json())
if response.status_code == 200:
    # Get needed data from the JSON response
    data = response.json()
    for article in data['data']:
        try:
            insert_article_to_sqlite(article)
        except Exception as e:
            logging.error(f"Failed to insert article to SQLite: {e}")
else:
    logging.error(f"Failed to fetch news from Mediastack: {response.json()}")