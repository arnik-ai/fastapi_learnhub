from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

def _convert_refs(data: Dict[str, Any]) -> Dict[str, Any]:
    # convert FK strings to ObjectId if present and valid
    for fk in ("student_id", "course_id"):
        if fk in data and isinstance(data[fk], str) and ObjectId.is_valid(data[fk]):
            data[fk] = ObjectId(data[fk])
    return data

async def create_enrollment(data: Dict[str, Any]) -> dict:
    coll = get_collection("enrollments")
    data = _convert_refs(data)
    result = await coll.insert_one(data)
    created = await coll.find_one({"_id": result.inserted_id})
    return serialize_doc(created)

async def get_enrollment_by_id(enrollment_id: str) -> Optional[dict]:
    coll = get_collection("enrollments")
    doc = await coll.find_one({"_id": _oid(enrollment_id)})
    return serialize_doc(doc)

async def list_enrollments(
    skip: int = 0,
    limit: int = 50,
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
) -> List[dict]:
    coll = get_collection("enrollments")
    query: Dict[str, Any] = {}
    if student_id:
        query["student_id"] = _oid(student_id)
    if course_id:
        query["course_id"] = _oid(course_id)
    cursor = coll.find(query, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]

async def update_enrollment(enrollment_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("enrollments")
    data = _convert_refs(data)
    await coll.update_one({"_id": _oid(enrollment_id)}, {"$set": data})
    return await get_enrollment_by_id(enrollment_id)

async def delete_enrollment(enrollment_id: str) -> bool:
    coll = get_collection("enrollments")
    res = await coll.delete_one({"_id": _oid(enrollment_id)})
    return res.deleted_count == 1
