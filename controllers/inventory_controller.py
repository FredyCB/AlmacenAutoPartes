from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection

def get_inventory(part_id: str = None):
    coll = get_collection("inventory")
    if part_id:
        try:
            pid = ObjectId(part_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid part id")
        docs = list(coll.find({"part_id": pid}))
    else:
        docs = list(coll.find())
    # convert ids to str
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
        if "part_id" in d and isinstance(d["part_id"], ObjectId):
            d["part_id"] = str(d["part_id"])
    return docs

def add_inventory(data: dict):
    try:
        data["part_id"] = ObjectId(data["part_id"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part id")
    coll = get_collection("inventory")
    res = coll.insert_one(data)
    return {"message": "Inventory added", "id": str(res.inserted_id)}

def update_stock(item_id: str, quantity: int):
    try:
        _id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid inventory id")
    coll = get_collection("inventory")
    r = coll.update_one({"_id": _id}, {"$set": {"quantity": quantity}})
    if r.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"message": "Stock updated"}

def low_stock_items(threshold: int = 10):
    coll = get_collection("inventory")
    docs = list(coll.find({"quantity": {"$lt": threshold}}))
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs
