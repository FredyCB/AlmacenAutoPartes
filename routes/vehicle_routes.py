from fastapi import APIRouter, Request
from models.vehicle import Vehicle
from controllers.vehicles_controller import create_vehicle, get_vehicles
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/")
@validateadmin
async def create_vehicle_endpoint(vehicle: Vehicle, request: Request):
    return await create_vehicle(vehicle)

@router.get("/")
@validateuser
async def get_vehicles_endpoint():
    return await get_vehicles()
