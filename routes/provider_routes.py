from fastapi import APIRouter, Request
from models.provider import Provider
from controllers.provider_controller import (
    create_provider,
    get_providers,

    update_provider,
)
from utils.security import validateadmin

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.post("/", response_model=Provider)
@validateadmin
async def create_provider_endpoint(request: Request, provider: Provider) -> Provider:
    return await create_provider(provider)


@router.get("/", response_model=list[Provider])
@validateadmin
async def list_providers_endpoint() -> list[Provider]:
    return await get_providers()

@router.put("/{provider_id}", response_model=dict)
@validateadmin
async def update_provider_endpoint(provider_id: str, provider: Provider, request: Request) -> dict:
    return await update_provider(provider_id, provider)
