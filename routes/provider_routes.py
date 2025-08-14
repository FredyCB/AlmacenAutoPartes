from fastapi import APIRouter, Request
from models.provider import Provider
from controllers.provider_controller import create_provider, get_providers, get_provider_by_id, update_provider, delete_provider
from utils.security import validateadmin

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", response_model=dict)
@validateadmin
async def create_provider_endpoint(request: Request, provider: Provider):
    return create_provider(provider.model_dump(exclude={"id"}))

@router.get("/", response_model=list)
async def list_providers_endpoint():
    return get_providers()

@router.get("/{provider_id}", response_model=dict)
async def get_provider_endpoint(provider_id: str):
    return get_provider_by_id(provider_id)

@router.put("/{provider_id}", response_model=dict)
@validateadmin
async def update_provider_endpoint(request: Request, provider_id: str, provider: Provider):
    return update_provider(provider_id, provider.model_dump(exclude={"id"}))

@router.delete("/{provider_id}", response_model=dict)
@validateadmin
async def delete_provider_endpoint(request: Request, provider_id: str):
    return delete_provider(provider_id)
