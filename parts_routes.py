from fastapi import APIRouter, Request, HTTPException
from models.part import Part
from models.vehicle_part import VehiclePart
from controllers.parts_controller import (
    create_part, get_part_by_id, update_part, delete_part, add_compatibility, get_compatibility
)
from utils.security import validateadmin

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post("/", response_model=dict)
@validateadmin
async def create_part_endpoint(request: Request, part: Part):
    return create_part(part.model_dump(exclude={"id"}))

@router.get("/{part_id}", response_model=dict)
async def get_part_endpoint(part_id: str):
    return get_part_by_id(part_id)

@router.put("/{part_id}", response_model=dict)
@validateadmin
async def update_part_endpoint(request: Request, part_id: str, data: dict):
    return update_part(part_id, data)

@router.delete("/{part_id}", response_model=dict)
@validateadmin
async def delete_part_endpoint(request: Request, part_id: str):
    return delete_part(part_id)

@router.get("/{part_id}/compatibility", response_model=list)
async def get_compatibility_endpoint(part_id: str):
    return get_compatibility(part_id)

@router.post("/{part_id}/compatibility", response_model=dict)
@validateadmin
async def add_compatibility_endpoint(request: Request, part_id: str, compat: VehiclePart):
    return add_compatibility(part_id, compat.vehicle_id)
