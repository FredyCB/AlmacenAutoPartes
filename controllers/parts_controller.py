from fastapi import HTTPException, status
from bson import ObjectId
from models.parts import PartOut, PartWithProvider
from pipelines.parts_pipelines import (
    parts_with_providers,
    parts_statistics,
    validate_provider_usage
)
from utils.db import db

# Añadir estos nuevos métodos
async def get_parts_with_providers():
    """Obtiene partes con info de proveedor (Pipeline $lookup)"""
    cursor = db["parts"].aggregate(parts_with_providers())
    return [PartWithProvider(**doc) async for doc in cursor]

async def get_parts_stats():
    """Obtiene estadísticas (Pipeline $group)"""
    cursor = db["parts"].aggregate(parts_statistics())
    return await cursor.to_list(None)

async def validate_provider_delete(provider_id: str):
    """Valida si un proveedor puede eliminarse (Pipeline validación)"""
    result = await db["parts"].aggregate(
        validate_provider_usage(provider_id)
    ).to_list(1)
    
    if result and result[0]["total_parts"] > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proveedor tiene {result[0]['total_parts']} partes asociadas",
            headers={"X-Parts-Asociadas": ",".join(result[0]["parts_list"])}
        )
