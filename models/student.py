from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: Optional[int] = None

class StudentResponse(Student):
    id: str
