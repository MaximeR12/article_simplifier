import ollama
import json
import os
import secrets
from fastapi import FastAPI, Security, Response, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

TOKENS_FILE = "../tokens.json"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")

def load_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

def generate_token():
    return secrets.token_urlsafe(32)

# Ensure the tokens file exists and load tokens
if not os.path.exists(TOKENS_FILE):
    with open(TOKENS_FILE, "w") as f:
        json.dump({}, f)

tokens = load_tokens()

if not tokens:
    initial_token = generate_token()
    tokens[initial_token] = {"user_id": "initial_user"}
    save_tokens(tokens)
    print(f"Initial token generated: {initial_token}")

app = FastAPI()

class Script(BaseModel):
    script: str

class Token(BaseModel):
    user_id : int
    token: str

security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    tokens = load_tokens()
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[token]["user_id"]


@app.post("/article_analyse")
async def ollama_chat(article: Script, language: str = "ENG", user_id: str = Depends(authenticate)):
    try:
        logger.debug(f"Received request for article analysis. Language: {language}, User ID: {user_id}")
        logger.debug(f"Article content: {article.script[:100]}...")  # Log first 100 characters of the article
        
        output = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': f"""Context: You are an article analysis assistant. Your task is to provide a synthetic version of the input article and translate it if needed.

            1. Summarize the following article in a concise manner, capturing the main points and key information:
            {article.script}

            2. If the requested language is different from the article's original language, translate the summary to {language}.

            Please provide the synthetic version (and translation if applicable) of the article."""
            }]
        )
        logger.debug(f"Ollama chat response received. Content length: {len(output['message']['content'])}")
        return output['message']['content']
    except Exception as e:
        logger.exception(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/create_token")
async def create_token(admin_token: str, user_id: str):
    if admin_token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid admin token")
    new_token = generate_token()
    tokens[new_token] = {"user_id": user_id}
    save_tokens(tokens)
    return {"token": new_token}

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)