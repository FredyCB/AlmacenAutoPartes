from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from controllers.parts_controller import *
from models.parts_model import *
from utils.auth import get_current_user

router = APIRouter(prefix="/parts", tags=["parts"])

@router.get("/with_proveedor", response_model=List[PartWithProveedor])
async def list_parts_with_proveedor():
    """Obtiene parts con información de proveedor (usando $lookup)"""
    return await get_parts_with_proveedor()

@router.get("/stats")
async def get_stats():
    """Estadísticas agregadas por categoría"""
    return await get_parts_stats()

@router.get("/search", response_model=List[PartWithProveedor])
async def search_parts(
    categoria: Optional[str] = Query(None),
    precio_min: Optional[float] = Query(None),
    precio_max: Optional[float] = Query(None)
):
    """Búsqueda con filtros (accesible sin token)"""
    return await search_parts(categoria, precio_min, precio_max)
