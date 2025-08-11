from fastapi import HTTPException, status
from bson import ObjectId
from typing import Optional, List
from models.parts_model import *
from models.proveedor_model import ProveedorOut
from pipelines.parts_pipelines import *
from utils.db import db
from utils.auth import get_current_user

async def validar_referencias(part: PartIn):
    # Validar proveedor
    if not await db["proveedores"].find_one({"_id": ObjectId(part.proveedor_id)}):
        raise HTTPException(status_code=400, detail="Proveedor no existe")
    
    # Validar categoría
    if not await db["categorias"].find_one({"nombre": part.categoria}):
        raise HTTPException(status_code=400, detail="Categoría no existe")

async def create_part(part: PartIn, usuario_actual: dict):
    await validar_referencias(part)
    
    part_dict = part.dict()
    part_dict["proveedor_id"] = ObjectId(part_dict["proveedor_id"])
    part_dict["creado_por"] = usuario_actual["email"]
    
    nuevo = await db["parts"].insert_one(part_dict)
    creado = await db["parts"].find_one({"_id": nuevo.inserted_id})
    return PartOut(**creado)

async def get_parts_with_proveedor():
    cursor = db["parts"].aggregate(pipeline_parts_proveedor())
    return [PartWithProveedor(**doc) async for doc in cursor]

async def get_parts_stats():
    cursor = db["parts"].aggregate(pipeline_estadisticas())
    return [doc async for doc in cursor]
