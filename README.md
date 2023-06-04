# FastAPI Proxy for Pinconce Vector DB

This FastAPI application serves as a proxy for forwarding requests to a Pinconce vector database. It provides a
convenient interface to interact with the database by allowing users to run queries based on vectorized queries.

## Features

- Proxy requests to a Pinconce vector database
- Run queries based on vectorized queries
- Customizable configuration options

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-proxy-pinconce-db.git
cd fastapi-proxy-pinconce-db
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate # For Linux/Mac
env\Scripts\activate # For Windows
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root directory and configure the following environment variables:

```dotenv
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=your_chosen_algorithm
PINCONCE_DB_URL=your_pinconce_db_url
PINCONCE_API_KEY=your_api_key
```

Replace `your_pinconce_db_url` with the URL of your Pinconce vector database and `your_api_key` with the API key for
authentication.

5. Run the application:

```bash
uvicorn main:app --reload
```

The FastAPI application will start running on `http://localhost:8000`.

## Usage

1. Make a `POST` request to the `/query` endpoint using your preferred HTTP client (e.g., cURL, Postman, or
   Python's `requests` library).

Example cURL command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query_vector": [0.1, 0.2, 0.3]}' http://localhost:8000/query
```

This example sends a JSON payload with the `query_vector` containing the vectorized query.

2. The application will forward the request to the Pinconce vector database, retrieve the results based on the provided
   query vector, and return the response to the client.

## Configuration

The application can be configured by modifying the settings in the `config.py` file. You can customize parameters such
as the database URL, API key, authentication mechanism, logging settings, and more.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, feel free to
open an issue or submit a pull request.

Please make sure to follow the code style and include appropriate tests for any changes you propose.

## License

This project is licensed under the [MIT License](LICENSE.md).
