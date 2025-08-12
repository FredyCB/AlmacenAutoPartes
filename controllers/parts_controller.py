from fastapi import HTTPException
from bson import ObjectId
from models.part import Part
from models.vehicle_part import VehiclePart
from utils.mongodb import get_collection

parts_coll = get_collection("catalog")
compatibility_coll = get_collection("vehicle_parts")

async def create_part(part: Part) -> Part:
    try:
        part_dict = part.model_dump(exclude={"id"})
        result = parts_coll.insert_one(part_dict)
        part.id = str(result.inserted_id)
        return part
    except Exception as e:
        raise HTTPException(500, f"Error creating part: {e}")

async def get_part_by_id(part_id: str) -> dict:
    if not ObjectId.is_valid(part_id):
        raise HTTPException(400, "Invalid ID format")
    part = parts_coll.find_one({"_id": ObjectId(part_id)})
    if not part:
        raise HTTPException(404, "Part not found")
    part["id"] = str(part["_id"])
    del part["_id"]
    return part

async def update_part(part_id: str, data: dict) -> dict:
    if not ObjectId.is_valid(part_id):
        raise HTTPException(400, "Invalid ID format")
    result = parts_coll.update_one({"_id": ObjectId(part_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(404, "Part not found")
    return {"message": "Part updated successfully"}

async def delete_part(part_id: str) -> dict:
    if not ObjectId.is_valid(part_id):
        raise HTTPException(400, "Invalid ID format")
    result = parts_coll.update_one({"_id": ObjectId(part_id)}, {"$set": {"active": False}})
    if result.matched_count == 0:
        raise HTTPException(404, "Part not found")
    return {"message": "Part disabled"}

async def get_compatibility(part_id: str) -> list:
    return list(compatibility_coll.find({"id_part": part_id}))

async def add_compatibility(part_id: str, compat: VehiclePart) -> dict:
    compat.id_part = part_id
    data = compat.model_dump(exclude={"id"})
    result = compatibility_coll.insert_one(data)
    return {"message": "Compatibility added", "id": str(result.inserted_id)}

