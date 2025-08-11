from fastapi import APIRouter, Request, Query
from models.inventory import Inventory
from controllers.inventory_controller import add_inventory, get_inventory, update_stock, low_stock_items
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/catalogo", tags=["Inventory"])

@router.post("/", summary="Agregar item inventario (admin)")
@validateadmin
async def add_inventory_endpoint(request: Request, item: Inventory):
    return add_inventory(item.model_dump(exclude_none=True))

@router.get("/", summary="Consultar stock por repuesto (publico)")
async def get_inventory_endpoint(part_id: str = Query(None, description="ID de parte (ObjectId)")):
    return get_inventory(part_id)

@router.put("/{inventory_id}/stock", summary="Ajustar stock (admin)")
@validateadmin
async def update_stock_endpoint(request: Request, inventory_id: str, quantity: int):
    return update_stock(inventory_id, quantity)

@router.get("/low-stock", summary="Items con stock bajo (admin)")
@validateadmin
async def low_stock_endpoint(request: Request, threshold: int = 10):
    return low_stock_items(threshold)
