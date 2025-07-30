from fastapi import APIRouter, Request
from models.inventory import Inventory
from controllers.inventory_controller import (
    add_inventory, get_inventory_by_part, update_stock, get_low_stock_items
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/catalogo", tags=["Inventory"])

@router.post("/")
@validateadmin
async def add_inventory_endpoint(request: Request, item: Inventory):
    return await add_inventory(item)

@router.get("/")
@validateuser
async def get_inventory_by_part_endpoint(part_id: str):
    return await get_inventory_by_part(part_id)

@router.put("/{inventory_id}/stock")
@validateadmin
async def update_stock_endpoint(inventory_id: str, quantity: int):
    return await update_stock(inventory_id, quantity)

@router.get("/low-stock")
@validateadmin
async def get_low_stock_items_endpoint():
    return await get_low_stock_items()
