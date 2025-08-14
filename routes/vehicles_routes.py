from fastapi import APIRouter, Request
from models.vehicle import Vehicle
from controllers.vehicles_controller import create_vehicle, get_vehicles
from utils.security import validateadmin

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=dict)
@validateadmin
async def create_vehicle_endpoint(request: Request, vehicle: Vehicle):
    return create_vehicle(vehicle.model_dump(exclude={"id"}))

@router.get("/", response_model=list)
async def get_vehicles_endpoint():
    return get_vehicles()