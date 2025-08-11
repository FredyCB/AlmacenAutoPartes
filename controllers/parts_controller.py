from fastapi import HTTPException, status
from bson import ObjectId
from models.parts import Part, PartCreate, PartWithProvider
from models.proveedor import Proveedor
from pipelines.parts_pipelines import parts_with_providers, parts_stats, validate_provider_usage
from utils.db import db
from utils.auth import get_current_user

async def create_part(part: PartCreate, user: dict = Depends(get_current_user)):
    # Validar existencia del proveedor
    if not await db["proveedores"].find_one({"_id": ObjectId(part.proveedor_id)}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El proveedor no existe"
        )

    part_data = part.dict()
    part_data["creado_por"] = user["email"]
    inserted = await db["parts"].insert_one(part_data)
    return await db["parts"].find_one({"_id": inserted.inserted_id})

async def get_parts_with_providers():
    """Endpoint con Pipeline 1 ($lookup)"""
    cursor = db["parts"].aggregate(parts_with_providers())
    return [PartWithProvider(**doc) async for doc in cursor]

async def get_parts_statistics():
    """Endpoint con Pipeline 2 ($group)"""
    cursor = db["parts"].aggregate(parts_stats())
    return [doc async for doc in cursor]

async def search_parts(
    categoria: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 10
):
    """Endpoint con QueryString (accesible sin token)"""
    query = {}
    if categoria:
        query["categoria"] = categoria
    if min_price or max_price:
        query["precio"] = {}
        if min_price:
            query["precio"]["$gte"] = min_price
        if max_price:
            query["precio"]["$lte"] = max_price
    
    return await db["parts"].find(query).skip(skip).limit(limit).to_list(limit)
