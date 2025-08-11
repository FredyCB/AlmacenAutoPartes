from fastapi import APIRouter, Query
from controllers.search_controller import search_parts, cross_reference_search

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", summary="Buscar repuestos (public)")
async def search_endpoint(q: str = Query(..., description="Texto búsqueda"), skip: int = 0, limit: int = 20):
    return search_parts(q, skip, limit)

@router.get("/cross-reference", summary="Buscar por ref cruzada (public)")
async def cross_reference_endpoint(ref: str = Query(...)):
    return cross_reference_search(ref)
