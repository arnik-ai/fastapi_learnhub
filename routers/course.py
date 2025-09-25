from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from crud.course import (
    create_course, get_course_by_id, list_courses,
    update_course, delete_course
)

router = APIRouter()

class CourseCreate(BaseModel):
    code: str = Field(..., examples=["CS101"])
    title: str
    credits: int = Field(ge=0, le=10)
    teacher_id: Optional[str] = None  # store as ObjectId string
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    credits: Optional[int] = Field(default=None, ge=0, le=10)
    teacher_id: Optional[str] = None
    description: Optional[str] = None

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_course(payload: CourseCreate):
    if payload.teacher_id:
        _check_oid(payload.teacher_id)
    return await create_course(payload.model_dump())

@router.get("/")
async def get_courses(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200)):
    return await list_courses(skip=skip, limit=limit)

@router.get("/{course_id}")
async def get_course(course_id: str):
    _check_oid(course_id)
    found = await get_course_by_id(course_id)
    if not found:
        raise HTTPException(404, "Course not found")
    return found

@router.patch("/{course_id}")
async def patch_course(course_id: str, payload: CourseUpdate):
    _check_oid(course_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if "teacher_id" in data and data["teacher_id"]:
        _check_oid(data["teacher_id"])
    updated = await update_course(course_id, data)
    if not updated:
        raise HTTPException(404, "Course not found")
    return updated

@router.delete("/{course_id}", status_code=204)
async def remove_course(course_id: str):
    _check_oid(course_id)
    ok = await delete_course(course_id)
    if not ok:
        raise HTTPException(404, "Course not found")
