import os
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "http://mrowell-llm-api.francecentral.azurecontainer.io:8001")
LLM_API_TOKEN = os.getenv("LLM_API_TOKEN")

def analysis(input_text, output_language):
    payload = {
        "article": input_text,
        "language": output_language
    }
    response = requests.post(f"{LLM_API_URL}/article_analyse/", json=payload, headers={"Authorization": f"Bearer {LLM_API_TOKEN}"})
    print(response.status_code)
    print(response.json())
    return response.json()
