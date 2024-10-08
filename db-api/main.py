import os
from psycopg2 import connect
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional

# Get the database connection details from the environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
api_token = os.getenv('DB_API_TOKEN')

# Dependency to verify the token
def verify_token(x_token: str = Header(...)):
    if x_token != api_token:
        raise HTTPException(status_code=401, detail="Invalid token")

# Establish a connection to the database
try:
    connection = connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    cursor = connection.cursor()
    print("Database connection established")
except Exception as e:
    connection = None
    cursor = None
    print(f"Failed to connect to the database: {e}")

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

# Define a Pydantic model for the LLM Call Log
class LLMCallLog(BaseModel):
    model: str
    input: str
    output: str
    response_time: float
    user_satisfaction: Optional[int] = None

# Create a new analysis (CREATE)
@app.post("/analysis/", dependencies=[Depends(verify_token)])
async def create_analysis(analysis: Analysis):
    if cursor:
        cursor.execute("""
            INSERT INTO analysis (user_id, content, result, analysis_duration, is_satisfied)
            VALUES (%s, %s, %s, %s, %s)
        """, (analysis.user_id, analysis.content, analysis.result, analysis.analysis_duration, analysis.is_satisfied))
        connection.commit()
        return {"message": "Analysis created"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.get("/analysis/", dependencies=[Depends(verify_token)])
async def get_analyses():
    if cursor:
        cursor.execute("SELECT * FROM analysis")
        rows = cursor.fetchall()
        return [{"id": row[0], "user_id": row[1], "content": row[2], "result": row[3], "timestamp": row[4], "analysis_duration": row[5], "is_satisfied": row[6]} for row in rows]
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.get("/analysis/{analysis_id}", dependencies=[Depends(verify_token)])
async def get_analysis(analysis_id: int):
    if cursor:
        cursor.execute("SELECT * FROM analysis WHERE id = %s", (analysis_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return {"id": row[0], "user_id": row[1], "content": row[2], "result": row[3], "timestamp": row[4], "analysis_duration": row[5], "is_satisfied": row[6]}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.put("/analysis/{analysis_id}", dependencies=[Depends(verify_token)])
async def update_analysis(analysis_id: int, analysis: Analysis):
    if cursor:
        cursor.execute("""
            UPDATE analysis
            SET user_id = %s, content = %s, result = %s, analysis_duration = %s, is_satisfied = %s
            WHERE id = %s
        """, (analysis.user_id, analysis.content, analysis.result, analysis.analysis_duration, analysis.is_satisfied, analysis_id))
        connection.commit()
        return {"message": "Analysis updated"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.delete("/analysis/{analysis_id}", dependencies=[Depends(verify_token)])
async def delete_analysis(analysis_id: int):
    if cursor:
        cursor.execute("DELETE FROM analysis WHERE id = %s", (analysis_id,))
        connection.commit()
        return {"message": "Analysis deleted"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.post("/article/", dependencies=[Depends(verify_token)])
async def create_article(article: Article):
    if cursor:
        cursor.execute("""
            INSERT INTO article (source, title, content, language)
            VALUES (%s, %s, %s, %s)
        """, (article.source, article.title, article.content, article.language))
        connection.commit()
        return {"message": "Article created"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

# Get all articles (READ)
@app.get("/article/", dependencies=[Depends(verify_token)])
async def get_articles():
    if cursor:
        cursor.execute("SELECT * FROM article")
        rows = cursor.fetchall()
        return [{"id": row[0], "source": row[1], "title": row[2], "content": row[3], "language": row[4], "timestamp": row[5]} for row in rows]
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

# Get a specific article by ID (READ)
@app.get("/article/{article_id}", dependencies=[Depends(verify_token)])
async def get_article(article_id: int):
    if cursor:
        cursor.execute("SELECT * FROM article WHERE id = %s", (article_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"id": row[0], "source": row[1], "title": row[2], "content": row[3], "language": row[4], "timestamp": row[5]}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

# Update a specific article by ID (UPDATE)
@app.put("/article/{article_id}", dependencies=[Depends(verify_token)])
async def update_article(article_id: int, article: Article):
    if cursor:
        cursor.execute("""
            UPDATE article
            SET source = %s, title = %s, content = %s, language = %s
            WHERE id = %s
        """, (article.source, article.title, article.content, article.language, article_id))
        connection.commit()
        return {"message": "Article updated"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

# Delete a specific article by ID (DELETE)
@app.delete("/article/{article_id}", dependencies=[Depends(verify_token)])
async def delete_article(article_id: int):
    if cursor:
        cursor.execute("DELETE FROM article WHERE id = %s", (article_id,))
        connection.commit()
        return {"message": "Article deleted"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

# Create a new LLM call log
@app.post("/llm_call_log/", dependencies=[Depends(verify_token)])
async def create_llm_call_log(log: LLMCallLog):
    if cursor:
        cursor.execute("""
            INSERT INTO llm_call_logs (model, input, output, response_time, user_satisfaction)
            VALUES (%s, %s, %s, %s, %s)
        """, (log.model, log.input, log.output, log.response_time, log.user_satisfaction))
        connection.commit()
        return {"message": "LLM call log created"}
    else:
        raise HTTPException(status_code=500, detail="Database connection not available")

@app.get("/health")
async def health():
    return {"status": "ok"}

