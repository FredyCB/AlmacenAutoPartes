from fastapi import APIRouter, Query
from controllers.search_controller import (
    search_parts_by_name_or_description,
    search_by_cross_reference
)

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=list[dict])
async def search_parts(query: str = Query(..., description="Texto de búsqueda")):
    return await search_parts_by_name_or_description(query)


@router.get("/cross-reference", response_model=list[dict])
async def search_cross_reference(ref: str = Query(..., description="Número de referencia cruzada")):
    return await search_by_cross_reference(ref)
