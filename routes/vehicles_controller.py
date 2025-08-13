# controllers/vehicle_controller.py
from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection

COL = "vehicles"

def create_vehicle(data: dict):
    coll = get_collection(COL)
    res = coll.insert_one(data)
    return {"message": "Vehicle created", "id": str(res.inserted_id)}

def get_vehicles():
    coll = get_collection(COL)
    docs = list(coll.find({"active": True}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs
