from fastapi import APIRouter, Request
from models.vehicle import Vehicle
from controllers.vehicles_controller import (
    create_vehicle,
    get_vehicles,

)
from utils.security import validateadmin

router = APIRouter()

@router.post("/vehicles", tags=["Vehicles"])
@validateadmin
async def create_vehicle_endpoint(vehicle: Vehicle, request: Request):
    return await create_vehicle(vehicle)

@router.get("/vehicles", tags=["Vehicles"])
async def get_vehicles_endpoint():
    return await get_vehicles()


