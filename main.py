import psycopg2
from dotenv import load_dotenv
import os
from database import init_db, get_all_persons, get_person_by_name

# Load environment variables
load_dotenv()

# Initialize the database and sample data
init_db()

# Fetch and display a specific person
person = get_person_by_name('John Doe')
if person:
    print(person)

# Fetch and display all persons
all_persons = get_all_persons()
for person in all_persons:
    print(person)

print("\nTo run the FastAPI server, use: uvicorn api:app --reload")