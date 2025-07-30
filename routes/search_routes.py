from fastapi import APIRouter, Query
from controllers.search_controller import search_parts_by_name_or_description

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search_parts(query: str = Query(..., description="Texto de búsqueda")):
    return await search_parts_by_name_or_description(query)