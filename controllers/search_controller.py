from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from models.parts import PartOut
from pipelines.parts_pipelines import search_pipeline
from utils.db import db
from utils.security import allow_without_token

router = APIRouter()

@router.get(
    "/parts/search",
    response_model=List[PartOut],
    dependencies=[Depends(allow_without_token)],
    description="Búsqueda de partes accesible sin token (QueryString)"
)
async def search_parts(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    skip: int = 0,
    limit: int = 10
):
    pipeline = search_pipeline(category, min_price, max_price)
    pipeline.extend([
        {"$skip": skip},
        {"$limit": limit}
    ])
    
    try:
        cursor = db["parts"].aggregate(pipeline)
        return await cursor.to_list(length=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en búsqueda: {str(e)}"
        )
