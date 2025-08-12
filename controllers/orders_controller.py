from fastapi import HTTPException
from bson import ObjectId
from models.order import Order
from utils.mongodb import get_collection

orders_coll = get_collection("orders")

async def reserve_order(order: Order) -> dict:
    order_dict = order.model_dump(exclude={"id"})
    order_dict["status"] = "reserved"
    inserted = orders_coll.insert_one(order_dict)
    return {"message": "Order reserved", "order_id": str(inserted.inserted_id)}

async def confirm_order(order: Order) -> dict:
    order_dict = order.model_dump(exclude={"id"})
    order_dict["status"] = "confirmed"
    inserted = orders_coll.insert_one(order_dict)
    return {"message": "Order confirmed", "order_id": str(inserted.inserted_id)}

async def cancel_order(order_id: str) -> dict:
    if not ObjectId.is_valid(order_id):
        raise HTTPException(400, "Invalid ID")
    result = orders_coll.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": "cancelled"}})
    if result.matched_count == 0:
        raise HTTPException(404, "Order not found")
    return {"message": "Order cancelled"}

async def get_orders_by_client(client_id: str) -> list:
    return list(orders_coll.find({"client_id": client_id}))
