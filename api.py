from fastapi import FastAPI, HTTPException, Depends
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