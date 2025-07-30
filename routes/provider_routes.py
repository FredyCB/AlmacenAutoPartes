from fastapi import APIRouter, Request
from models.provider import Provider
from controllers.provider_controller import create_provider
from utils.security import validateadmin

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", response_model=Provider)
@validateadmin
async def create_provider_endpoint(request: Request, provider: Provider):
    return await create_provider(provider)