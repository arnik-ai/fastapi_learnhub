from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

async def create_teacher(data: Dict[str, Any]) -> dict:
    coll = get_collection("teachers")
    result = await coll.insert_one(data)
    created = await coll.find_one({"_id": result.inserted_id})
    return serialize_doc(created)

async def get_teacher_by_id(teacher_id: str) -> Optional[dict]:
    coll = get_collection("teachers")
    doc = await coll.find_one({"_id": _oid(teacher_id)})
    return serialize_doc(doc)

async def list_teachers(skip: int = 0, limit: int = 50) -> List[dict]:
    coll = get_collection("teachers")
    cursor = coll.find({}, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]

async def update_teacher(teacher_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("teachers")
    await coll.update_one({"_id": _oid(teacher_id)}, {"$set": data})
    return await get_teacher_by_id(teacher_id)

async def delete_teacher(teacher_id: str) -> bool:
    coll = get_collection("teachers")
    res = await coll.delete_one({"_id": _oid(teacher_id)})
    return res.deleted_count == 1
