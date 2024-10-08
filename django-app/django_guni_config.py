import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

chdir = "/django-app/myapp"
bind = '0.0.0.0:8002'
wsgi_app = "myapp.wsgi"
workers = 4
timeout = 300
raw_env = [
    f"{key}={value}" for key, value in os.environ.items() if "DB" in key or "DJANGO" in key
]