from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection

COL = "providers"

def create_provider(data: dict):
    coll = get_collection(COL)
    res = coll.insert_one(data)
    return {"message": "Provider created", "id": str(res.inserted_id)}

def get_providers():
    coll = get_collection(COL)
    docs = list(coll.find({}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs

def get_provider_by_id(provider_id: str):
    try:
        _id = ObjectId(provider_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(COL)
    doc = coll.find_one({"_id": _id})
    if not doc:
        raise HTTPException(status_code=404, detail="Provider not found")
    doc["id"] = str(doc["_id"]); del doc["_id"]
    return doc

def update_provider(provider_id: str, data: dict):
    try:
        _id = ObjectId(provider_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(COL)
    res = coll.update_one({"_id": _id}, {"$set": data})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider updated"}

def delete_provider(provider_id: str):
    try:
        _id = ObjectId(provider_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(COL)
    res = coll.delete_one({"_id": _id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted"}
