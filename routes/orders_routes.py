from fastapi import APIRouter, Request
from models.order import Order
from controllers.orders_controller import reserve_order, confirm_order, cancel_order, get_orders_by_client
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/reserve", response_model=dict)
async def reserve_order_endpoint(order: Order):
    # public: clients don't need admin
    return reserve_order(order.model_dump(exclude={"id"}))

@router.post("/", response_model=dict)
async def confirm_order_endpoint(order: Order):
    return confirm_order(order.model_dump(exclude={"id"}))

@router.put("/{order_id}/cancel", response_model=dict)
async def cancel_order_endpoint(order_id: str):
    return cancel_order(order_id)

@router.get("/client/{client_id}", response_model=list)
@validateuser
async def get_orders_by_client_endpoint(request: Request, client_id: str):
    # users/admin can request
    return get_orders_by_client(client_id)
