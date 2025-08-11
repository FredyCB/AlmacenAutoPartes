from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection
from models.part import Part

parts_coll = get_collection("catalog")

def create_part(data: dict):
    # data viene del route (pydantic Part o dict)
    if isinstance(data, Part):
        doc = data.model_dump(exclude={"id"})
    else:
        doc = data
    result = parts_coll.insert_one(doc)
    return {"message": "Part created", "id": str(result.inserted_id)}

def get_part_by_id(part_id: str):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part id")
    doc = parts_coll.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Part not found")
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def update_part(part_id: str, data: dict):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part id")
    result = parts_coll.update_one({"_id": _id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part updated"}

def delete_part(part_id: str):
    try:
        _id = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part id")
    result = parts_coll.update_one({"_id": _id}, {"$set": {"active": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part deactivated"}

def add_compatibility(part_id: str, vehicle_id: str):
    try:
        _pid = ObjectId(part_id)
        _vid = ObjectId(vehicle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ids")
    coll = get_collection("vehicle_parts")
    coll.insert_one({"part_id": _pid, "vehicle_id": _vid})
    return {"message": "Compatibility added"}
