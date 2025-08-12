from fastapi import APIRouter, Request
from models.category import Category
from controllers.category_controller import (
    create_category, get_category_by_id, get_all_categories,
    update_category, delete_category
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=Category)
@validateadmin
async def create_category_endpoint(request: Request, category: Category):
    return await create_category(category)

@router.get("/", response_model=list[Category])
@validateuser
async def get_all_categories_endpoint():
    return await get_all_categories()

@router.get("/{category_id}", response_model=Category)
@validateuser
async def get_category_by_id_endpoint(category_id: str):
    return await get_category_by_id(category_id)

@router.put("/{category_id}")
@validateadmin
async def update_category_endpoint(category_id: str, data: dict):
    return await update_category(category_id, data)

@router.delete("/{category_id}")
@validateadmin
async def delete_category_endpoint(category_id: str):
    return await delete_category(category_id)