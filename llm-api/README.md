# Ollama LLM Model API

This repository contains a FastAPI application for analyzing articles using the Ollama LLM model.

## Overview

The API provides endpoints for analyzing articles, managing tokens, and health checks. It uses the Ollama library for language model interactions and logs the analysis results to a database.

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
    ```sh
    git clone git@github.com:MaximeR12/LLM-API.git
    cd LLM-API
    ```

2. **Install dependencies:**
    ```sh
    pip install -r llmrequirements.txt
    ```

3. **Set up environment variables:**
    Create a `.env` file in the `llm-api` directory with the following content:
    ```env
    OLLAMA_MODEL=llama3.2:3b
    DB_API_URL=http://localhost:8000
    DB_API_TOKEN=your_db_api_token
    ADMIN_TOKEN=your_admin_token
    ```

4. **Run the FastAPI server:**
    ```sh
    uvicorn main.main:app --host 0.0.0.0 --port 8001 --reload
    ```

### Docker Deployment

1. **Build the Docker image:**
    ```sh
    docker build -t ollama-llm-api .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d -p 8001:8001 --env-file .env ollama-llm-api
    ```

## API Endpoints

### Analyze Article

- **URL:** `/article_analyse`
- **Method:** `POST`
- **Description:** Analyzes an article and translates the summary into the specified language.
- **Request Body:**
    ```json
    {
        "article": "string",
        "language": "string"
    }
    ```
- **Response:**
    ```json
    {
        "summary": "string"
    }
    ```

### Create Token

- **URL:** `/create_token`
- **Method:** `POST`
- **Description:** Creates a new token for a user.
- **Request Body:**
    ```json
    {
        "admin_token": "string",
        "user_id": "string"
    }
    ```
- **Response:**
    ```json
    {
        "token": "string"
    }
    ```

### Health Check

- **URL:** `/health`
- **Method:** `GET`
- **Description:** Checks the health status of the API.
- **Response:**
    ```json
    {
        "status": "healthy"
    }
    ```

## Logging

The application logs various events and errors. Logs are sent to the database using the `send_logs_to_db` function.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
