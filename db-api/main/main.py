from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from setup import env_path
import psycopg2
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv(env_path)

# Get the database connection details from the environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')

# Establish a connection to the database
connection = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host
)

# Create a cursor object
cursor = connection.cursor()

# Create a FastAPI app
app = FastAPI()

# Define a Pydantic model for the Analysis table
class Analysis(BaseModel):
    user_id: int
    content: str
    result: str
    analysis_duration: str
    is_satisfied: bool

# Define a Pydantic model for the Article table
class Article(BaseModel):
    source: str
    title: str
    content: str
    language: str

# Create a new analysis (CREATE)
@app.post("/analysis/")
async def create_analysis(analysis: Analysis):
    cursor.execute("""
        INSERT INTO analysis (user_id, content, result, analysis_duration, is_satisfied)
        VALUES (%s, %s, %s, %s, %s)
    """, (analysis.user_id, analysis.content, analysis.result, analysis.analysis_duration, analysis.is_satisfied))
    connection.commit()
    return {"message": "Analysis created"}

# Get all analyses (READ)
@app.get("/analysis/")
async def get_analyses():
    cursor.execute("SELECT * FROM analysis")
    rows = cursor.fetchall()
    return [{"id": row[0], "user_id": row[1], "content": row[2], "result": row[3], "timestamp": row[4], "analysis_duration": row[5], "is_satisfied": row[6]} for row in rows]

# Get a specific analysis by ID (READ)
@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: int):
    cursor.execute("SELECT * FROM analysis WHERE id = %s", (analysis_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"id": row[0], "user_id": row[1], "content": row[2], "result": row[3], "timestamp": row[4], "analysis_duration": row[5], "is_satisfied": row[6]}

# Update a specific analysis by ID (UPDATE)
@app.put("/analysis/{analysis_id}")
async def update_analysis(analysis_id: int, analysis: Analysis):
    cursor.execute("""
        UPDATE analysis
        SET user_id = %s, content = %s, result = %s, analysis_duration = %s, is_satisfied = %s
        WHERE id = %s
    """, (analysis.user_id, analysis.content, analysis.result, analysis.analysis_duration, analysis.is_satisfied, analysis_id))
    connection.commit()
    return {"message": "Analysis updated"}

# Delete a specific analysis by ID (DELETE)
@app.delete("/analysis/{analysis_id}")
async def delete_analysis(analysis_id: int):
    cursor.execute("DELETE FROM analysis WHERE id = %s", (analysis_id,))
    connection.commit()
    return {"message": "Analysis deleted"}

# Create a new article (CREATE)
@app.post("/article/")
async def create_article(article: Article):
    cursor.execute("""
        INSERT INTO article (source, title, content, language)
        VALUES (%s, %s, %s, %s)
    """, (article.source, article.title, article.content, article.language))
    connection.commit()
    return {"message": "Article created"}

# Get all articles (READ)
@app.get("/article/")
async def get_articles():
    cursor.execute("SELECT * FROM article")
    rows = cursor.fetchall()
    return [{"id": row[0], "source": row[1], "title": row[2], "content": row[3], "language": row[4], "timestamp": row[5]} for row in rows]

# Get a specific article by ID (READ)
@app.get("/article/{article_id}")
async def get_article(article_id: int):
    cursor.execute("SELECT * FROM article WHERE id = %s", (article_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"id": row[0], "source": row[1], "title": row[2], "content": row[3], "language": row[4], "timestamp": row[5]}

# Update a specific article by ID (UPDATE)
@app.put("/article/{article_id}")
async def update_article(article_id: int, article: Article):
    cursor.execute("""
        UPDATE article
        SET source = %s, title = %s, content = %s, language = %s
        WHERE id = %s
    """, (article.source, article.title, article.content, article.language, article_id))
    connection.commit()
    return {"message": "Article updated"}

# Delete a specific article by ID (DELETE)
@app.delete("/article/{article_id}")
async def delete_article(article_id: int):
    cursor.execute("DELETE FROM article WHERE id = %s", (article_id,))
    connection.commit()
    return {"message": "Article deleted"}
