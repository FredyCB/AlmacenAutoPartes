from bson import ObjectId
from fastapi import HTTPException
from utils.mongodb import get_collection
from models.vehicle import Vehicle

coll = get_collection("vehicles")

def create_vehicle(data: dict):
    if isinstance(data, Vehicle):
        doc = data.model_dump(exclude={"id"})
    else:
        doc = data
    r = coll.insert_one(doc)
    return {"message":"Vehicle created","id":str(r.inserted_id)}

def get_vehicles():
    docs = list(coll.find({"active":True}))
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs
