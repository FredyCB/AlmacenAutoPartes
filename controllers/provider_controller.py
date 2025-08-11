from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection
from models.provider import Provider

coll = get_collection("providers")

def create_provider(data: dict):
    if isinstance(data, Provider):
        doc = data.model_dump(exclude={"id"})
    else:
        doc = data
    res = coll.insert_one(doc)
    return {"message": "Provider created", "id": str(res.inserted_id)}

def get_providers():
    docs = list(coll.find())
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs

def update_provider(provider_id: str, data: dict):
    try:
        _id = ObjectId(provider_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid provider id")
    r = coll.update_one({"_id": _id}, {"$set": data})
    if r.matched_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider updated"}

def delete_provider(provider_id: str):
    try:
        _id = ObjectId(provider_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid provider id")
    r = coll.delete_one({"_id": _id})
    if r.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {"message": "Provider deleted"}
