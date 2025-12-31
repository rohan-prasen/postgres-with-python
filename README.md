# Learning PostgreSQL with Python & FastAPI

Hey, I am learning how to use PostgreSQL with Python for backend development. This project now includes a FastAPI application to serve data through a REST API.

## Setup

```bash
# For those who prefer HTTPS
git clone https://github.com/rohan-prasen/postgres-with-python.git

# For those who prefer SSH
git clone git@github.com:rohan-prasen/postgres-with-python.git
```

```bash
# I used uv as my venv manager
uv sync
./.venv/Scripts/activate # windows
source ./.venv/bin/activate # macOS/Linux

# Normal python venv usage
# For windows users
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt

# For macOS/Linux users
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
```

## Before running the code don't forget to create a `.env` file

```bash
cp .env.example .env
```

### Your .env file looks as follows

```env
DB_HOST="localhost"
DB_DATABASE="postgres"
DB_USER="postgres"
DB_PASSWORD="your-password-here"
DB_PORT=5432
```

Change all the environment variables in the .env file and then try to run the program using the commands below.

## Running the Application

### Run the original script (database operations):
```bash
# To run the original database operations script
uv run main.py
```

### Run the FastAPI server:
```bash
# Method 1: Using uvicorn directly
uv run uvicorn api:app --reload

# Method 2: Using the main_api.py file
uv run python main_api.py

# Method 3: Using the server.py file
uv run python server.py
```

## API Endpoints

Once the server is running, you can access the following endpoints:

- `GET /` - Root endpoint with status information
- `GET /persons/` - Get all persons
- `GET /persons/{person_id}` - Get a specific person by ID
- `GET /persons/search?name={name}` - Search persons by name (partial matching)
- `POST /persons/` - Create a new person
- `PUT /persons/{person_id}` - Update an existing person
- `DELETE /persons/{person_id}` - Delete a person
- `GET /health` - Health check endpoint
- `GET /test` - Simple test endpoint to verify the API is working
- `GET /stats` - Get statistics about the database
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## API Models

### Person Object
- `id` (integer): Unique identifier
- `name` (string): Person's name
- `age` (integer): Person's age
- `gender` (string): Person's gender (single character)

Example:
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 30,
  "gender": "M"
}
```
