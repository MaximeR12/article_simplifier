# FastAPI Script Analyzer

This repository contains scripts for analyzing SQL scripts using FastAPI and the Ollama library.

## Getting Started

To get started, follow these instructions:

1. **Clone the repository:**
    ```sh
    git clone git@github.com:MaximeR12/LLM-API.git
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Create a token:**
    You'll need a token to authenticate requests. Run the following command to generate a token:
    ```sh
    python create_token.py <username>
    ```

4. **Run the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```

## Scripts

### `main.py`

This script sets up a FastAPI app to analyze SQL scripts. It defines routes for analyzing scripts and authenticating users using tokens.

### `create_token.py`

This script generates a token for a given username. Tokens are used for authentication when accessing the FastAPI endpoints.

### `test_api.py`

This script contains unit tests for the FastAPI endpoints. It includes tests for script analysis and token generation.

## Usage

### Analyzing a Script

To analyze a script, send a POST request to `/script_analyse` with a JSON body containing the script and a valid token in the Authorization header.

Example request:
```json
{
  "script": "INSERT INTO test_target FROM test_source"
}
```
## Running Tests

To run the unit tests, execute the following command:

```sh
python test_api.py
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
