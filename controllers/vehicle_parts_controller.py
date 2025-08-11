from bson import ObjectId
from fastapi import HTTPException
from utils.mongodb import get_collection
from models.vehicle_part import VehiclePart

coll = get_collection("vehicle_parts")

def link_part_to_vehicle(data: dict):
    if isinstance(data, VehiclePart):
        doc = data.model_dump(exclude={"id"})
    else:
        doc = data
    try:
        doc["vehicle_id"] = ObjectId(doc["vehicle_id"])
        doc["part_id"] = ObjectId(doc["part_id"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ids")
    r = coll.insert_one(doc)
    return {"message":"Linked","id":str(r.inserted_id)}

def get_parts_by_vehicle(vehicle_id: str):
    try:
        vid = ObjectId(vehicle_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid vehicle id")
    docs = list(coll.find({"vehicle_id": vid}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
        d["vehicle_id"] = str(d["vehicle_id"]); d["part_id"] = str(d["part_id"])
    return docs

def get_vehicles_by_part(part_id: str):
    try:
        pid = ObjectId(part_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part id")
    docs = list(coll.find({"part_id": pid}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
        d["vehicle_id"] = str(d["vehicle_id"]); d["part_id"] = str(d["part_id"])
    return docs

def delete_link(link_id: str):
    try:
        _id = ObjectId(link_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")
    r = coll.delete_one({"_id": _id})
    if r.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message":"Deleted"}
