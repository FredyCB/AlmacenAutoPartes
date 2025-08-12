from fastapi import APIRouter
from models.order import Order
from controllers.orders_controller import (
    reserve_order, confirm_order, cancel_order, get_orders_by_client
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/reserve")
@validateuser
async def reserve_order_endpoint(order: Order):
    return await reserve_order(order)

@router.post("/confirm")
@validateadmin
async def confirm_order_endpoint(order: Order):
    return await confirm_order(order)

@router.delete("/cancel/{order_id}")
@validateadmin
async def cancel_order_endpoint(order_id: str):
    return await cancel_order(order_id)

@router.get("/by-client/{client_id}")
@validateuser
async def get_orders_by_client_endpoint(client_id: str):
    return await get_orders_by_client(client_id)
