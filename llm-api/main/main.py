import ollama
import json
import os
from fastapi import FastAPI, Security, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel


def read_tokens_from_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({"tokens": {}}, file)
    with open(file_path, "r") as file:
        config = json.load(file)
    return config.get("tokens", {})

tokens_config_path = "main/tokens.json"
app = FastAPI()

class Script(BaseModel):
    script: str

class Token(BaseModel):
    user_id : int
    token: str

security = HTTPBearer()

def authenticate(token):
    valid_users = read_tokens_from_file(tokens_config_path)
    if token not in valid_users.values():
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


@app.post("/script_analyse")
async def ollama_chat(script: Script):
    output = ollama.chat(
      model='llama3:8b',
      messages=[{'role': 'user', 'content': f"""Context : You are a Data lineage assistant, you help a data steward by creating a csv file that lists all source/target relations between tables of a sql script.
      The csv file must follow this structure:
      source_schema,source_tabletarget_schema,target_table
                 
        Analyse this script : {script}"""
        }]
    )
    return output['message']['content']


# @app.post("/script_analyse")
# async def ollama_chat(script: Script, token: HTTPAuthorizationCredentials = Security(security)):
#     if not authenticate(token.credentials):
#         return Response(status_code=401, content="Unauthorized")
#     output = ollama.chat(
#       model='llama3:8b',
#       messages=[{'role': 'user', 'content': """Context : You are a Data lineage assistant, you help a data steward by creating a csv file that lists all source/target relations between tables of a sql script.
#       The csv file must follow this structure :
#       source_schema, source_table, target_schema, target_table
      
#       List all source/target relations between the different tables of this sql script:"""+ script.script +". The output you provide should only contain the csv content"
#                   }])
#     return output['message']['content']