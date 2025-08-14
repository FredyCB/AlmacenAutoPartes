from fastapi import APIRouter, Request
from models.vehicle_part import VehiclePart
from controllers.vehicle_parts_controller import link_part_to_vehicle, get_parts_by_vehicle, get_vehicles_by_part, delete_vehicle_part_link
from utils.security import validateadmin

router = APIRouter(prefix="/vehicleparts", tags=["Vehicle-Part Links"])

@router.post("/", response_model=dict)
@validateadmin
async def link_part_endpoint(request: Request, data: VehiclePart):
    return link_part_to_vehicle(data.model_dump(exclude={"id"}))

@router.get("/vehicle/{vehicle_id}", response_model=list)
async def get_parts_by_vehicle_endpoint(vehicle_id: str):
    return get_parts_by_vehicle(vehicle_id)

@router.get("/part/{part_id}", response_model=list)
async def get_vehicles_by_part_endpoint(part_id: str):
    return get_vehicles_by_part(part_id)

@router.delete("/{link_id}", response_model=dict)
@validateadmin
async def delete_link_endpoint(request: Request, link_id: str):
    return delete_vehicle_part_link(link_id)