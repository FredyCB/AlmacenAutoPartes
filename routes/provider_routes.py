from fastapi import APIRouter, Request
from models.provider import Provider
from controllers.provider_controller import create_provider, get_providers, update_provider, delete_provider
from utils.security import validateadmin

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", summary="Crear proveedor (admin)")
@validateadmin
async def create_provider_endpoint(request: Request, provider: Provider):
    return create_provider(provider)

@router.get("/", summary="Listar proveedores (admin)")
@validateadmin
async def list_providers_endpoint():
    return get_providers()

@router.put("/{provider_id}", summary="Actualizar proveedor (admin)")
@validateadmin
async def update_provider_endpoint(provider_id: str, provider: Provider, request: Request):
    return update_provider(provider_id, provider.model_dump(exclude_none=True))

@router.delete("/{provider_id}", summary="Eliminar proveedor (admin)")
@validateadmin
async def delete_provider_endpoint(provider_id: str, request: Request):
    return delete_provider(provider_id)
