from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection
from pipelines.inventory import inventory_with_parts_pipeline

COL = "inventory"

def add_inventory(data: dict):
    try:
        # assume data['part_id'] is string of ObjectId
        ObjectId(data["part_id"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid part_id")
    coll = get_collection(COL)
    res = coll.insert_one(data)
    return {"message": "Inventory item added", "id": str(res.inserted_id)}

def get_inventory_by_part(part_id: str):
    coll = get_collection(COL)
    items = list(coll.find({"part_id": part_id}))
    for it in items:
        it["id"] = str(it["_id"]); del it["_id"]
    return items

def update_stock(item_id: str, quantity: int):
    try:
        _id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(COL)
    res = coll.update_one({"_id": _id}, {"$set": {"quantity": quantity}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"message": "Stock updated"}

def get_low_stock_items(threshold: int = 10):
    coll = get_collection(COL)
    items = list(coll.find({"quantity": {"$lt": threshold}}))
    for it in items:
        it["id"] = str(it["_id"]); del it["_id"]
    return items
