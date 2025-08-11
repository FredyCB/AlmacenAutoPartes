from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from controllers.parts import *
from models.parts import Part, PartWithProvider
from utils.auth import get_current_user

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post("/", response_model=Part)
async def create_part_endpoint(part: PartCreate, user: dict = Depends(get_current_user)):
    return await create_part(part, user)

@router.get("/with_providers", response_model=List[PartWithProvider])
async def get_parts_with_providers_endpoint():
    """Obtiene parts con info de proveedor (Pipeline $lookup)"""
    return await get_parts_with_providers()

@router.get("/stats")
async def get_stats_endpoint():
    """Estadísticas agregadas (Pipeline $group)"""
    return await get_parts_statistics()

@router.get("/search", response_model=List[Part])
async def search_parts_endpoint(
    categoria: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    """Búsqueda con filtros (accesible sin token)"""
    return await search_parts(categoria, min_price, max_price, skip, limit)
