from fastapi import HTTPException
from bson import ObjectId
from utils.mongodb import get_collection
from models.order import Order

orders_coll = get_collection("orders")
inventory_coll = get_collection("inventory")

def reserve_order(order_data: dict):
    # order_data is dict or pydantic Order
    # Basic validation & reserve stock
    try:
        items = order_data.get("items", [])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order data")
    # check stock for each item
    for it in items:
        pid = ObjectId(it["part_id"])
        inv = inventory_coll.find_one({"part_id": pid})
        if not inv or inv.get("quantity",0) < it["quantity"]:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for part {it.get('part_id')}")
    # reduce stock (simple implementation)
    for it in items:
        pid = ObjectId(it["part_id"])
        inventory_coll.update_one({"part_id": pid}, {"$inc": {"quantity": -int(it["quantity"])}})
    # insert reserved order
    order_data["status"] = "reserved"
    res = orders_coll.insert_one(order_data)
    return {"message": "Order reserved", "id": str(res.inserted_id)}

def confirm_order(order_data: dict):
    order_data["status"] = "confirmed"
    res = orders_coll.insert_one(order_data)
    return {"message": "Order confirmed", "id": str(res.inserted_id)}

def cancel_order(order_id: str):
    try:
        _id = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order id")
    r = orders_coll.update_one({"_id": _id}, {"$set": {"status": "cancelled"}})
    if r.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order cancelled"}

def get_orders_by_client(client_id: str):
    coll = get_collection("orders")
    try:
        uid = ObjectId(client_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid client id")
    docs = list(coll.find({"user_id": uid}))
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs
