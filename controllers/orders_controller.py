from models.order import Order
from utils.mongodb import get_collection

orders_coll = get_collection("orders")

async def reserve_order(order: Order) -> dict:
    order_dict = order.model_dump(exclude={"id"})
    order_dict["status"] = "reserved"
    inserted = orders_coll.insert_one(order_dict)
    return {"message": "Order reserved", "order_id": str(inserted.inserted_id)}

async def get_orders_by_client(client_id: str) -> list:
    return list(orders_coll.find({"id_user": client_id}))
