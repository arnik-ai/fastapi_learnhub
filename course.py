from pydantic import BaseModel, Field
from typing import Optional

class Course(BaseModel):
    code: str = Field(..., examples=["CS101"])
    title: str
    credits: int = Field(ge=0, le=10)
    teacher_id: Optional[str] = None  # ObjectId as string
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    credits: Optional[int] = Field(default=None, ge=0, le=10)
    teacher_id: Optional[str] = None
    description: Optional[str] = None
