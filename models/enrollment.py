from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Enrollment(BaseModel):
    student_id: str  # ObjectId string
    course_id: str   # ObjectId string
    semester: str = Field(..., examples=["Fall 2025"])
    status: Optional[str] = Field(default="active", examples=["active", "dropped", "completed"])
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)

class EnrollmentResponse(Enrollment):
    id: str
