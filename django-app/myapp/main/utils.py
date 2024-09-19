import requests

def analysis(input_text: str, output_language: str = 'ENG'):
    api_url = "http://your-api-endpoint/analysis/"  # Replace with your actual API endpoint
    
    payload = {
        "content": input_text,
        "language": output_language
    }
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        result = response.json()
        return result.get("result", "No result found")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return "Error occurred while processing the request"