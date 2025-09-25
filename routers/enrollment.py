from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from crud.enrollment import (
    create_enrollment, get_enrollment_by_id, list_enrollments,
    update_enrollment, delete_enrollment
)

router = APIRouter()

class EnrollmentCreate(BaseModel):
    student_id: str  # ObjectId string
    course_id: str   # ObjectId string
    semester: str = Field(..., examples=["Fall 2025"])
    status: Optional[str] = Field(default="active", examples=["active", "dropped", "completed"])

class EnrollmentUpdate(BaseModel):
    student_id: Optional[str] = None
    course_id: Optional[str] = None
    semester: Optional[str] = None
    status: Optional[str] = None

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_enrollment(payload: EnrollmentCreate):
    _check_oid(payload.student_id)
    _check_oid(payload.course_id)
    return await create_enrollment(payload.model_dump())

@router.get("/")
async def get_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
):
    if student_id: _check_oid(student_id)
    if course_id: _check_oid(course_id)
    return await list_enrollments(skip=skip, limit=limit, student_id=student_id, course_id=course_id)

@router.get("/{enrollment_id}")
async def get_enrollment(enrollment_id: str):
    _check_oid(enrollment_id)
    found = await get_enrollment_by_id(enrollment_id)
    if not found:
        raise HTTPException(404, "Enrollment not found")
    return found

@router.patch("/{enrollment_id}")
async def patch_enrollment(enrollment_id: str, payload: EnrollmentUpdate):
    _check_oid(enrollment_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if "student_id" in data: _check_oid(data["student_id"])
    if "course_id" in data: _check_oid(data["course_id"])
    updated = await update_enrollment(enrollment_id, data)
    if not updated:
        raise HTTPException(404, "Enrollment not found")
    return updated

@router.delete("/{enrollment_id}", status_code=204)
async def remove_enrollment(enrollment_id: str):
    _check_oid(enrollment_id)
    ok = await delete_enrollment(enrollment_id)
    if not ok:
        raise HTTPException(404, "Enrollment not found")
