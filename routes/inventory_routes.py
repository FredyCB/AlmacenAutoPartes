from fastapi import APIRouter, Request, Query
from models.inventory import Inventory
from controllers.inventory_controller import add_inventory, get_inventory_by_part, update_stock, get_low_stock_items
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/catalogo", tags=["Inventory"])

@router.post("/", response_model=dict)
@validateadmin
async def add_inventory_endpoint(request: Request, item: Inventory):
    return add_inventory(item.model_dump(exclude={"id"}))

@router.get("/", response_model=list)
async def get_inventory_for_part(part_id: str = Query(...)):
    return get_inventory_by_part(part_id)

@router.put("/{inventory_id}/stock", response_model=dict)
@validateadmin
async def update_stock_endpoint(request: Request, inventory_id: str, quantity: int = Query(...)):
    return update_stock(inventory_id, quantity)

@router.get("/low-stock", response_model=list)
@validateadmin
async def low_stock_endpoint(request: Request):
    return get_low_stock_items()
