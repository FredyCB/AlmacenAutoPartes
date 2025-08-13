from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection
from datetime import datetime

ORDERS = "orders"
INVENTORY = "inventory"

def reserve_order(order_data: dict):
    # reduce stock (simple, no transaction)
    coll_orders = get_collection(ORDERS)
    coll_inventory = get_collection(INVENTORY)

    # Validate and reduce stock
    for item in order_data.get("items", []):
        part_id = item["part_id"]
        qty = item["quantity"]
        # find inventory item for that part (first one with enough stock)
        inv = coll_inventory.find_one({"part_id": part_id, "quantity": {"$gte": qty}})
        if not inv:
            raise HTTPException(status_code=400, detail=f"No stock suficiente para part {part_id}")
        coll_inventory.update_one({"_id": inv["_id"]}, {"$inc": {"quantity": -qty}})

    order_data["status"] = "reserved"
    order_data["date"] = datetime.utcnow()
    res = coll_orders.insert_one(order_data)
    return {"message": "Order reserved", "order_id": str(res.inserted_id)}

def confirm_order(order_data: dict):
    coll_orders = get_collection(ORDERS)
    order_data["status"] = "confirmed"
    order_data["date"] = datetime.utcnow()
    res = coll_orders.insert_one(order_data)
    return {"message": "Order confirmed", "order_id": str(res.inserted_id)}

def cancel_order(order_id: str):
    try:
        _id = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    coll = get_collection(ORDERS)
    order = coll.find_one({"_id": _id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # release stock if reserved
    if order.get("status") == "reserved":
        coll_inventory = get_collection(INVENTORY)
        for item in order.get("items", []):
            coll_inventory.update_one({"part_id": item["part_id"]}, {"$inc": {"quantity": item["quantity"]}})
    coll.update_one({"_id": _id}, {"$set": {"status": "cancelled"}})
    return {"message": "Order cancelled"}

def get_orders_by_client(client_id: str):
    coll = get_collection(ORDERS)
    docs = list(coll.find({"client_id": client_id}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs