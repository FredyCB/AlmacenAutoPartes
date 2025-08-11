from fastapi import APIRouter, Request
from models.vehicle import Vehicle
from controllers.vehicle_controller import create_vehicle, get_vehicles
from utils.security import validateadmin

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", summary="Crear vehículo (admin)")
@validateadmin
async def create_vehicle_endpoint(request: Request, vehicle: Vehicle):
    return create_vehicle(vehicle.model_dump(exclude_none=True))

@router.get("/", summary="Listar vehículos (public)")
async def list_vehicles_endpoint():
    return get_vehicles()
