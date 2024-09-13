import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from setup import env_path

# Get the database connection details from the environment variables
load_dotenv(find_dotenv())

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
print(db_host)

# connection to the database & creating a cursor
connection = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host)

cursor = connection.cursor()

# analysis table creation
cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        model TEXT,
        content TEXT,
        result TEXT,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        analysis_duration INTERVAL,
        is_satisfied BOOLEAN
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS article (
        id SERIAL PRIMARY KEY,
        source TEXT,
        title TEXT,
        content TEXT,
        language TEXT,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
""")

connection.commit()
cursor.close()
connection.close()

print("Tables creation process completed.")