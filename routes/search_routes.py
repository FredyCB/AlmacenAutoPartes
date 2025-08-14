from fastapi import APIRouter, Query
from controllers.search_controller import search_parts_by_name_or_description, cross_reference_search

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=list)
async def search_parts(query: str = Query(...), skip: int = 0, limit: int = 20):
    return search_parts_by_name_or_description(query, skip, limit)

@router.get("/cross-reference", response_model=list)
async def search_cross_reference(ref: str = Query(...)):
    return cross_reference_search(ref)
