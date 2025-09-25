from pydantic import BaseModel, EmailStr
from typing import Optional

class Teacher(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: Optional[str] = None

class TeacherResponse(Teacher):
    id: str
