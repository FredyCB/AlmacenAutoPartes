from fastapi import APIRouter, Request
from models.part import Part
from models.vehicle_part import VehiclePart
from controllers.parts_controller import create_part, get_part_by_id, update_part, delete_part, add_compatibility
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post("/", summary="Crear repuesto (admin)")
@validateadmin
async def create_part_endpoint(request: Request, part: Part):
    return create_part(part)

@router.get("/{part_id}", summary="Obtener repuesto por id")
async def get_part_endpoint(part_id: str):
    return get_part_by_id(part_id)

@router.put("/{part_id}", summary="Actualizar repuesto (admin)")
@validateadmin
async def update_part_endpoint(part_id: str, data: dict, request: Request):
    return update_part(part_id, data)

@router.delete("/{part_id}", summary="Desactivar repuesto (admin)")
@validateadmin
async def delete_part_endpoint(part_id: str, request: Request):
    return delete_part(part_id)

@router.get("/{part_id}/compatibility", summary="Listar compatibilidades")
async def get_compatibility_endpoint(part_id: str):
    # This route uses vehicle_parts collection
    from utils.mongodb import get_collection
    coll = get_collection("vehicle_parts")
    docs = list(coll.find({"part_id": part_id}))
    for d in docs:
        d["id"] = str(d["_id"]); del d["_id"]
    return docs

@router.post("/{part_id}/compatibility", summary="Agregar compatibilidad (admin)")
@validateadmin
async def add_compatibility_endpoint(part_id: str, compat: VehiclePart, request: Request):
    # compat.vehicle_id provided — ensure part_id matches
    return add_compatibility(part_id, compat.vehicle_id)
