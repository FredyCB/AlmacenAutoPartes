from utils.mongodb import get_collection
from models.vehicle import Vehicle
from bson import ObjectId

collection = get_collection("vehicles")

async def create_vehicle(data: Vehicle) -> dict:
    vehicle = data.model_dump(exclude={"id"})
    result = collection.insert_one(vehicle)
    return {"success": True, "data": str(result.inserted_id)}

async def get_vehicles() -> dict:
    vehicles = list(collection.find({"active": True}))
    for v in vehicles:
        v["id"] = str(v["_id"])
        del v["_id"]
    return {"success": True, "data": vehicles}
