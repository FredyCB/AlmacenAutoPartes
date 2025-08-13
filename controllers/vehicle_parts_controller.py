from fastapi import HTTPException
from utils.mongodb import get_collection

COL = "vehicle_parts"

def link_part_to_vehicle(data: dict):
    coll = get_collection(COL)
    # minimal duplicated check
    exists = coll.find_one({"vehicle_id": data["vehicle_id"], "part_id": data["part_id"]})
    if exists:
        return {"success": False, "message": "Relationship already exists"}
    res = coll.insert_one(data)
    return {"success": True, "id": str(res.inserted_id)}

def get_parts_by_vehicle(vehicle_id: str):
    coll = get_collection(COL)
    docs = list(coll.find({"vehicle_id": vehicle_id}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs

def get_vehicles_by_part(part_id: str):
    coll = get_collection(COL)
    docs = list(coll.find({"part_id": part_id}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs

def delete_vehicle_part_link(link_id: str):
    from bson import ObjectId
    try:
        _id = ObjectId(link_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(COL)
    res = coll.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"success": True}
