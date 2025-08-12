from fastapi import APIRouter, Request
from models.part import Part
from models.vehicle_part import VehiclePart
from controllers.parts_controller import (
    create_part, get_part_by_id, update_part, delete_part,
    get_compatibility, add_compatibility
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post("/", response_model=Part)
@validateadmin
async def create_part_endpoint(request: Request, part: Part):
    return await create_part(part)

@router.get("/{part_id}", response_model=dict)
@validateuser
async def get_part_by_id_endpoint(part_id: str):
    return await get_part_by_id(part_id)

@router.put("/{part_id}")
@validateadmin
async def update_part_endpoint(part_id: str, data: dict):
    return await update_part(part_id, data)

@router.delete("/{part_id}")
@validateadmin
async def delete_part_endpoint(part_id: str):
    return await delete_part(part_id)

@router.get("/{part_id}/compatibility")
@validateuser
async def get_compatibility_endpoint(part_id: str):
    return await get_compatibility(part_id)

@router.post("/{part_id}/compatibility")
@validateadmin
async def add_compatibility_endpoint(part_id: str, compat: VehiclePart):
    return await add_compatibility(part_id, compat)
