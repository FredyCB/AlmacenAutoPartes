from fastapi import APIRouter
from models.order import Order
from controllers.orders_controller import (
    reserve_order, get_orders_by_client
)
from utils.security import validateuser

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/reserve")
@validateuser
async def reserve_order_endpoint(order: Order):
    return await reserve_order(order)

@router.get("/client/{client_id}")
@validateuser
async def get_orders_by_client_endpoint(client_id: str):
    return await get_orders_by_client(client_id)
