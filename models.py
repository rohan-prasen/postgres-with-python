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