from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection

CATALOG = "catalog"
VEHICLE_PARTS = "vehicle_parts"

def create_part(data: dict):
    coll = get_collection(CATALOG)
    # No proporcionar id; mongodb generará _id
    res = coll.insert_one(data)
    return {"message": "Part created", "id": str(res.inserted_id)}

def get_part_by_id(part_id: str):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(CATALOG)
    doc = coll.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Part not found")
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def update_part(part_id: str, data: dict):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(CATALOG)
    res = coll.update_one({"_id": _id}, {"$set": data})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part updated"}

def delete_part(part_id: str):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(CATALOG)
    res = coll.update_one({"_id": _id}, {"$set": {"active": False}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part deactivated"}

def add_compatibility(part_id: str, vehicle_id: str):
    try:
        ObjectId(part_id)
        ObjectId(vehicle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid IDs")
    coll = get_collection(VEHICLE_PARTS)
    res = coll.insert_one({"part_id": part_id, "vehicle_id": vehicle_id})
    return {"message": "Compatibility added", "id": str(res.inserted_id)}

def get_compatibility(part_id: str):
    coll = get_collection(VEHICLE_PARTS)
    docs = list(coll.find({"part_id": part_id}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs
