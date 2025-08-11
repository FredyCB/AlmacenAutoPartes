from fastapi import HTTPException, status
from bson import ObjectId
from models.provider import ProviderOut
from pipelines.parts_pipelines import validate_provider_usage
from utils.db import db
from utils.security import get_admin_user

async def delete_provider(provider_id: str, admin: dict = Depends(get_admin_user)):
    """
    Elimina un proveedor solo si no tiene autopartes asociadas
    
    Args:
        provider_id: ID del proveedor a eliminar
        admin: Datos del administrador autenticado
        
    Returns:
        dict: Mensaje de confirmación
        
    Raises:
        HTTPException: Si el proveedor tiene autopartes asociadas
    """
    # Validación con pipeline
    cursor = db.parts.aggregate(validate_provider_usage(provider_id))
    result = await cursor.to_list(length=1)
    
    if result and result[0].get("total_parts", 0) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar, tiene {result[0]['total_parts']} autopartes asociadas",
            headers={"X-Parts-Asociadas": ",".join(result[0].get("parts_list", []))}
        )
    
    # Eliminación segura
    deleted = await db.providers.delete_one({"_id": ObjectId(provider_id)})
    if deleted.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    
    return {"message": "Proveedor eliminado correctamente"}
