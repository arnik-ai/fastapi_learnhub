from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional
from crud.teacher import (
    create_teacher, get_teacher_by_id, list_teachers,
    update_teacher, delete_teacher
)
from bson import ObjectId

router = APIRouter()

class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department: Optional[str] = None

class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_teacher(payload: TeacherCreate):
    return await create_teacher(payload.model_dump())

@router.get("/")
async def get_teachers(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200)):
    return await list_teachers(skip=skip, limit=limit)

@router.get("/{teacher_id}")
async def get_teacher(teacher_id: str):
    _check_oid(teacher_id)
    found = await get_teacher_by_id(teacher_id)
    if not found:
        raise HTTPException(404, "Teacher not found")
    return found

@router.patch("/{teacher_id}")
async def patch_teacher(teacher_id: str, payload: TeacherUpdate):
    _check_oid(teacher_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await update_teacher(teacher_id, data)
    if not updated:
        raise HTTPException(404, "Teacher not found")
    return updated

@router.delete("/{teacher_id}", status_code=204)
async def remove_teacher(teacher_id: str):
    _check_oid(teacher_id)
    ok = await delete_teacher(teacher_id)
    if not ok:
        raise HTTPException(404, "Teacher not found")
