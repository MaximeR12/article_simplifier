import requests

# Define the URL of the FastAPI endpoint
url = "http://0.0.0.0:8001/script_analyse"

# Define the headers, including the authorization token
headers = {
    "Content-Type": "application/json"
}

# Define the payload (the script you want to analyze)
payload = {
    "script": "SELECT * FROM source_table INTO target_table"
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response
print(response.status_code)
print(response.content)
