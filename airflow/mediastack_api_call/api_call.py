import requests
import os
import json

# Replace 'YOUR_API_KEY' with your actual Mediastack API key
api_key = '23bad5487cd57f506aeb4f15abd709f8'
params = {
    'access_key': api_key,
    'languages': 'fr',  # Fetch news in French
    'limit': 10,  # Limit the results to 10 articles
}

# Mediastack API endpoint for fetching news
url = 'http://api.mediastack.com/v1/news'

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Folder where the JSON file will be saved
    folder_name = '../data/raw'
    
    # Ensure the 'data' folder exists
    os.makedirs(folder_name, exist_ok=True)  # Creates the folder if it doesn't exist, does nothing otherwise
    
    # Path to the JSON file within the 'data' folder
    json_file_path = os.path.join(folder_name, 'news_articles.json')

    # Save the data to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    print(f"The JSON file was saved successfully at {json_file_path}.")
else:
    print("Failed to fetch data from Mediastack API, status code:", response.status_code)
