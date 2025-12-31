# Learning PostgreSQL with Python & FastAPI

This project demonstrates how to use PostgreSQL with Python for backend development, featuring a FastAPI application that serves data through a REST API. The implementation includes database operations, API endpoints, models, and server configuration with comprehensive documentation.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Environment Configuration](#environment-configuration)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
  - [Dependencies](#dependencies)
  - [Database Module](#database-module)
  - [Pydantic Models](#pydantic-models)
  - [FastAPI Application](#fastapi-application)
  - [Server Configuration](#server-configuration)
- [API Endpoints](#api-endpoints)
- [API Models](#api-models)
- [Running the Application](#running-the-application)
- [Testing the API](#testing-the-api)

## Overview

This project showcases the integration of PostgreSQL with Python using FastAPI to create a REST API. The application includes:

- Database operations with proper connection management
- CRUD operations for person records
- Search functionality
- Health checks
- Statistics endpoints
- Automatic API documentation

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

## Environment Configuration

Before running the code, create a `.env` file:

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

# Server configuration
HOST="0.0.0.0"
PORT=8000
RELOAD="True"
```

Change all the environment variables in the .env file and then try to run the program using the commands below.

## Project Structure

The project consists of the following key files:

- `main.py` - Original database operations script
- `api.py` - Main FastAPI application
- `database.py` - Database operations module
- `models.py` - Pydantic models for request/response validation
- `main_api.py` - Alternative entry point for running the API server
- `server.py` - Production-ready server configuration
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration

## Implementation Details

### Dependencies

The project includes the following dependencies:

#### requirements.txt

```txt
psycopg2
python-dotenv
fastapi>=0.104.1
uvicorn>=0.24.0
```

#### pyproject.toml

```toml
[project]
name = "postgres"
version = "0.1.0"
description = "I am learning Postgres with Python"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "psycopg2>=2.9.11",
    "python-dotenv>=1.2.1",
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
]
```

### Database Module

The database module handles all database operations with proper connection management:

#### database.py

```python
import psycopg2
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "melcowe"),
            port=os.getenv("DB_PORT", 5432)
        )
        yield conn
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize the database with the person table and sample data"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create table PERSON
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS person (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                gender CHAR(1) NOT NULL
                );
                """
            )

            # Insert sample data
            cur.execute(
                """
                INSERT INTO person (id, name, age, gender) VALUES
                (1, 'John Doe', 30, 'M'),
                (2, 'Jane Smith', 25, 'F'),
                (3, 'Alice Johnson', 28, 'F'),
                (4, 'Bob Brown', 35, 'M')
                ON CONFLICT (id) DO NOTHING;
                """
            )

            conn.commit()

def get_all_persons():
    """Get all persons from the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM person;')
            return cur.fetchall()

def get_person_by_id(person_id):
    """Get a person by ID from the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM person WHERE id = %s;', (person_id,))
            return cur.fetchone()

def get_person_by_name(name):
    """Get a person by name from the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM person WHERE name = %s;', (name,))
            return cur.fetchone()

def create_person(name, age, gender):
    """Create a new person in the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO person (name, age, gender)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (name, age, gender)
            )
            person_id = cur.fetchone()[0]
            conn.commit()
            return person_id

def update_person(person_id, name, age, gender):
    """Update a person in the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE person
                SET name = %s, age = %s, gender = %s
                WHERE id = %s;
                """,
                (name, age, gender, person_id)
            )
            conn.commit()

def delete_person(person_id):
    """Delete a person from the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM person WHERE id = %s;', (person_id,))
            conn.commit()
```

### Pydantic Models

Pydantic models provide request/response validation:

#### models.py

```python
from pydantic import BaseModel
from typing import Optional

class PersonBase(BaseModel):
    name: str
    age: int
    gender: str

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
```

### FastAPI Application

The main FastAPI application with comprehensive endpoints:

#### api.py

```python
from fastapi import FastAPI, HTTPException
from typing import List
import database
from models import Person, PersonCreate, PersonUpdate

# Initialize the database
database.init_db()

app = FastAPI(
    title="PostgreSQL Person API",
    description="""
    A FastAPI application to manage person records in PostgreSQL.

    ## Features
    - Create, read, update, and delete person records
    - Search functionality
    - Health checks
    - Automatic API documentation

    ## Usage
    - Use the /docs endpoint for interactive API documentation
    - Use the /redoc endpoint for alternative API documentation
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PostgreSQL Person API", "status": "running"}

@app.get("/persons/", response_model=List[Person])
def get_all_persons():
    """Get all persons from the database"""
    persons = database.get_all_persons()
    return [{"id": p[0], "name": p[1], "age": p[2], "gender": p[3]} for p in persons]

@app.get("/persons/{person_id}", response_model=Person)
def get_person(person_id: int):
    """Get a person by ID"""
    person = database.get_person_by_id(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"id": person[0], "name": person[1], "age": person[2], "gender": person[3]}

@app.get("/persons/search", response_model=List[Person])
def search_persons(name: str = None):
    """Search persons by name (partial matching)"""
    if name:
        # Using a simple approach - in a real app you might want to use ILIKE or full text search
        all_persons = database.get_all_persons()
        matching_persons = [p for p in all_persons if name.lower() in p[1].lower()]
        return [{"id": p[0], "name": p[1], "age": p[2], "gender": p[3]} for p in matching_persons]
    else:
        # If no name provided, return all persons
        all_persons = database.get_all_persons()
        return [{"id": p[0], "name": p[1], "age": p[2], "gender": p[3]} for p in all_persons]

@app.post("/persons/", response_model=Person)
def create_person(person: PersonCreate):
    """Create a new person"""
    person_id = database.create_person(person.name, person.age, person.gender)
    created_person = database.get_person_by_id(person_id)
    return {"id": created_person[0], "name": created_person[1], "age": created_person[2], "gender": created_person[3]}

@app.put("/persons/{person_id}", response_model=Person)
def update_person(person_id: int, person: PersonUpdate):
    """Update an existing person"""
    existing_person = database.get_person_by_id(person_id)
    if existing_person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    database.update_person(person_id, person.name, person.age, person.gender)
    updated_person = database.get_person_by_id(person_id)
    return {"id": updated_person[0], "name": updated_person[1], "age": updated_person[2], "gender": updated_person[3]}

@app.delete("/persons/{person_id}")
def delete_person(person_id: int):
    """Delete a person"""
    existing_person = database.get_person_by_id(person_id)
    if existing_person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    database.delete_person(person_id)
    return {"message": f"Person with ID {person_id} has been deleted"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Try to get a connection to verify database is accessible
        persons = database.get_all_persons()
        return {"status": "healthy", "database": "connected", "person_count": len(persons)}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/test")
def test_endpoint():
    """Simple test endpoint to verify the API is working"""
    return {"message": "API is working correctly!", "timestamp": __import__('datetime').datetime.now().isoformat()}

@app.get("/stats")
def get_stats():
    """Get statistics about the database"""
    persons = database.get_all_persons()
    gender_counts = {}
    age_sum = 0

    for person in persons:
        gender = person[3]  # gender is at index 3
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        age_sum += person[2]  # age is at index 2

    avg_age = age_sum / len(persons) if persons else 0

    return {
        "total_persons": len(persons),
        "gender_distribution": gender_counts,
        "average_age": round(avg_age, 2),
        "oldest_person": max([p[2] for p in persons]) if persons else None,
        "youngest_person": min([p[2] for p in persons]) if persons else None
    }
```

### Server Configuration

Server configuration files for different deployment scenarios:

#### main_api.py

```python
import uvicorn
import os
from api import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    print("Starting FastAPI server...")
    print("API documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    print(f"Server running on http://{host}:{port}")

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
```

#### server.py

```python
import uvicorn
from api import app
import os

def run_server():
    """Run the FastAPI server with uvicorn"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        debug=True,
        log_level="info",
        workers=1  # For development; in production you might want multiple workers
    )

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("API documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    print(f"Server running on http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', 8000)}")
    run_server()
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

## Running the Application

### Run the original script (database operations)

```bash
# To run the original database operations script
uv run main.py
```

### Run the FastAPI server

```bash
# Method 1: Using uvicorn directly
uv run uvicorn api:app --reload

# Method 2: Using the main_api.py file
uv run python main_api.py

# Method 3: Using the server.py file
uv run python server.py
```

## Testing the API

The API includes automatic interactive documentation at `/docs` and `/redoc` endpoints. You can also test the API endpoints directly:

1. Visit `http://localhost:8000/docs` for Swagger UI documentation
2. Visit `http://localhost:8000/redoc` for ReDoc documentation
3. Test the endpoints using curl or any HTTP client

Example curl commands:

```bash
# Get all persons
curl http://localhost:8000/persons/

# Get a specific person
curl http://localhost:8000/persons/1

# Search persons by name
curl "http://localhost:8000/persons/search?name=John"

# Create a new person
curl -X POST http://localhost:8000/persons/ \
  -H "Content-Type: application/json" \
  -d '{"name": "New Person", "age": 25, "gender": "F"}'

# Health check
curl http://localhost:8000/health

# Test endpoint
curl http://localhost:8000/test

# Statistics
curl http://localhost:8000/stats
```
