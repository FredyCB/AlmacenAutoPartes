from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from controllers.parts_controller import (
    create_part,
    get_part,
    update_part,
    delete_part,
    get_parts_with_providers,
    get_parts_stats,
    search_parts
)
from models.parts import PartCreate, PartOut, PartUpdate, PartWithProvider, PartStats
from utils.security import get_current_user

router = APIRouter(
    prefix="/parts",
    tags=["Parts"],
    responses={404: {"description": "No encontrado"}}
)

@router.post(
    "/",
    response_model=PartOut,
    status_code=201,
    summary="Crear nueva autoparte",
    description="Crea una nueva autoparte con validación de proveedor y categoría",
    responses={
        201: {"description": "Autoparte creada exitosamente"},
        400: {"description": "Validación fallida"},
        401: {"description": "No autorizado"}
    }
)
async def create_part_route(part: PartCreate, user: dict = Depends(get_current_user)):
    return await create_part(part, user)

@router.get(
    "/with-providers",
    response_model=List[PartWithProvider],
    summary="Listar autopartes con proveedores",
    description="Obtiene todas las autopartes con información de proveedores usando $lookup",
    responses={
        200: {"description": "Listado exitoso"},
        500: {"description": "Error en el servidor"}
    }
)
async def list_parts_with_providers_route():
    return await get_parts_with_providers()

@router.get(
    "/stats",
    response_model=List[PartStats],
    summary="Estadísticas de autopartes",
    description="Genera estadísticas agregadas por categoría usando $group",
    responses={
        200: {"example": [{"_id": "motor", "total_parts": 5, "avg_price": 125.50}]}
    }
)
async def get_parts_stats_route():
    return await get_parts_stats()

@router.get(
    "/search",
    response_model=List[PartOut],
    summary="Buscar autopartes",
    description="Endpoint público para filtrar autopartes por categoría y rango de precios",
    responses={
        200: {"description": "Búsqueda exitosa"},
        400: {"description": "Parámetros inválidos"}
    }
)
async def search_parts_route(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    skip: int = 0,
    limit: int = 10
):
    return await search_parts(category, min_price, max_price, skip, limit)
