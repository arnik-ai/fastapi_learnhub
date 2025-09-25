from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

def _convert_refs(data: Dict[str, Any]) -> Dict[str, Any]:
    # convert optional reference fields to ObjectId when valid
    for fk in ("teacher_id",):
        if fk in data and isinstance(data[fk], str) and ObjectId.is_valid(data[fk]):
            data[fk] = ObjectId(data[fk])
    return data

async def create_course(data: Dict[str, Any]) -> dict:
    coll = get_collection("courses")
    data = _convert_refs(data)
    result = await coll.insert_one(data)
    created = await coll.find_one({"_id": result.inserted_id})
    return serialize_doc(created)

async def get_course_by_id(course_id: str) -> Optional[dict]:
    coll = get_collection("courses")
    doc = await coll.find_one({"_id": _oid(course_id)})
    return serialize_doc(doc)

async def list_courses(skip: int = 0, limit: int = 50) -> List[dict]:
    coll = get_collection("courses")
    cursor = coll.find({}, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]

async def update_course(course_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("courses")
    data = _convert_refs(data)
    await coll.update_one({"_id": _oid(course_id)}, {"$set": data})
    return await get_course_by_id(course_id)

async def delete_course(course_id: str) -> bool:
    coll = get_collection("courses")
    res = await coll.delete_one({"_id": _oid(course_id)})
    return res.deleted_count == 1
