import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

LLM_API_URL = os.getenv("LLM_API_URL")
LLM_API_TOKEN = os.getenv("LLM_API_TOKEN")

def llm_api_call(input_text, output_language):
    payload = {
        "article": input_text,
        "language": output_language
    }
    try:
        response = requests.post(f"{LLM_API_URL}/article_analyse/", json=payload, headers={"Authorization": f"Bearer {LLM_API_TOKEN}"})
        response.raise_for_status()
        logger.info(f"Successful API call to LLM for language: {output_language}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error calling LLM API: {str(e)}")
        raise
