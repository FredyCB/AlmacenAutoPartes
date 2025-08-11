from fastapi import APIRouter, Depends
from controllers.parts_controller import (
    get_parts_with_providers,
    get_parts_stats
)
from models.parts import PartWithProvider

router = APIRouter(prefix="/parts", tags=["Parts"])

# Añadir estas nuevas rutas
@router.get(
    "/with-providers",
    response_model=List[PartWithProvider],
    description="Lista partes con información de proveedores (Pipeline $lookup)"
)
async def parts_providers_route():
    return await get_parts_with_providers()

@router.get(
    "/stats",
    description="Estadísticas de partes por categoría (Pipeline $group)"
)
async def parts_stats_route():
    return await get_parts_stats()
