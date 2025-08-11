from fastapi import HTTPException, status
from bson import ObjectId
from pipelines.parts_pipelines import validate_provider_usage

async def delete_proveedor(proveedor_id: str):
    # Validar con Pipeline 3
    cursor = db["parts"].aggregate(validate_provider_usage(proveedor_id))
    result = await cursor.to_list(length=1)
    
    if result and result[0]["total_parts"] > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proveedor tiene {result[0]['total_parts']} parts asociadas",
            headers={"X-Parts-Asociadas": ",".join(result[0]["parts_list"])}
        )
    
    deleted = await db["proveedores"].delete_one({"_id": ObjectId(proveedor_id)})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return {"message": "Proveedor eliminado correctamente"}
