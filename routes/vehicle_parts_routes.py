from fastapi import APIRouter, Request
from models.vehicle_part import VehiclePart
from controllers.vehicle_parts_controller import link_part_to_vehicle, get_parts_by_vehicle, get_vehicles_by_part, delete_link
from utils.security import validateadmin

router = APIRouter(prefix="/vehicleparts", tags=["Vehicle-Parts"])

@router.post("/", summary="Link part-vehicle (admin)")
@validateadmin
async def link_part_to_vehicle_endpoint(request: Request, data: VehiclePart):
    return link_part_to_vehicle(data)

@router.get("/vehicle/{vehicle_id}", summary="Partes por vehículo (public)")
async def parts_by_vehicle_endpoint(vehicle_id: str):
    return get_parts_by_vehicle(vehicle_id)

@router.get("/part/{part_id}", summary="Vehículos por parte (public)")
async def vehicles_by_part_endpoint(part_id: str):
    return get_vehicles_by_part(part_id)

@router.delete("/{link_id}", summary="Eliminar relación (admin)")
@validateadmin
async def delete_link_endpoint(request: Request, link_id: str):
    return delete_link(link_id)
