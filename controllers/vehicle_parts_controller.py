from utils.mongodb import get_collection
from models.vehicle_part import VehiclePart
from bson import ObjectId

collection = get_collection("vehicle_parts")

async def link_part_to_vehicle(data: VehiclePart) -> dict:
    relation = data.model_dump(exclude={"id"})
    exists = collection.find_one({
        "id_part": relation["id_part"],
        "id_vehicle": relation["id_vehicle"]
    })
    if exists:
        return {"success": False, "message": "Ya existe la relación entre esta parte y vehículo"}
    
    result = collection.insert_one(relation)
    return {"success": True, "data": str(result.inserted_id)}

async def get_parts_by_vehicle(vehicle_id: str) -> dict:
    results = list(collection.find({"id_vehicle": vehicle_id}))
    for r in results:
        r["id"] = str(r["_id"])
        del r["_id"]
    return {"success": True, "data": results}

async def get_vehicles_by_part(part_id: str) -> dict:
    results = list(collection.find({"id_part": part_id}))
    for r in results:
        r["id"] = str(r["_id"])
        del r["_id"]
    return {"success": True, "data": results}

async def delete_vehicle_part_link(link_id: str) -> dict:
    result = collection.delete_one({"_id": ObjectId(link_id)})
    if result.deleted_count == 0:
        return {"success": False, "message": "Relación no encontrada"}
    return {"success": True, "message": "Relación eliminada"}
