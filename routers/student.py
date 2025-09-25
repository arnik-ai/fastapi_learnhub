from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from crud.student import (
    create_student, get_student_by_id, list_students,
    update_student, delete_student
)
from bson import ObjectId

router = APIRouter()

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0, le=150)

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_student(payload: StudentCreate):
    return await create_student(payload.model_dump())

@router.get("/")
async def get_students(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200)):
    return await list_students(skip=skip, limit=limit)

@router.get("/{student_id}")
async def get_student(student_id: str):
    _check_oid(student_id)
    found = await get_student_by_id(student_id)
    if not found:
        raise HTTPException(404, "Student not found")
    return found

@router.patch("/{student_id}")
async def patch_student(student_id: str, payload: StudentUpdate):
    _check_oid(student_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await update_student(student_id, data)
    if not updated:
        raise HTTPException(404, "Student not found")
    return updated

@router.delete("/{student_id}", status_code=204)
async def remove_student(student_id: str):
    _check_oid(student_id)
    ok = await delete_student(student_id)
    if not ok:
        raise HTTPException(404, "Student not found")
