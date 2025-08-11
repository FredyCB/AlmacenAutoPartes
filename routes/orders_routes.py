from fastapi import APIRouter, Request
from models.order import Order
from controllers.orders_controller import reserve_order, confirm_order, cancel_order, get_orders_by_client
from utils.security import validateuser

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/reserve", summary="Reservar repuesto (public)")
async def reserve_order_endpoint(order: Order):
    return reserve_order(order.model_dump(exclude_none=True))

@router.post("/", summary="Confirmar orden (public)")
async def confirm_order_endpoint(order: Order):
    return confirm_order(order.model_dump(exclude_none=True))

@router.put("/{order_id}/cancel", summary="Cancelar orden (user)")
@validateuser
async def cancel_order_endpoint(request: Request, order_id: str):
    return cancel_order(order_id)

@router.get("/client/{client_id}", summary="Historial de cliente")
@validateuser
async def get_client_orders(request: Request, client_id: str):
    return get_orders_by_client(client_id)
