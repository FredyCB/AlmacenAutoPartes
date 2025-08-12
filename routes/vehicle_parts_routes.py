from fastapi import APIRouter, Request
from models.vehicle_part import VehiclePart
from controllers.vehicle_parts_controller import (
    link_part_to_vehicle,
    get_parts_by_vehicle,
    get_vehicles_by_part,
    delete_vehicle_part_link
)
from utils.security import validateadmin

router = APIRouter()

@router.post("/vehicleparts", tags=["Vehicle-Part Links"])
@validateadmin
async def link_part_to_vehicle_endpoint(data: VehiclePart, request: Request):
    return await link_part_to_vehicle(data)

@router.get("/vehicleparts/vehicle/{vehicle_id}", tags=["Vehicle-Part Links"])
async def get_parts_by_vehicle_endpoint(vehicle_id: str):
    return await get_parts_by_vehicle(vehicle_id)

@router.get("/vehicleparts/part/{part_id}", tags=["Vehicle-Part Links"])
async def get_vehicles_by_part_endpoint(part_id: str):
    return await get_vehicles_by_part(part_id)

@router.delete("/vehicleparts/{link_id}", tags=["Vehicle-Part Links"])
@validateadmin
async def delete_vehicle_part_link_endpoint(link_id: str, request: Request):
    return await delete_vehicle_part_link(link_id)
