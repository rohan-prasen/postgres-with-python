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