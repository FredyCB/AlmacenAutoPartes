from models.categoria import CategoriaCreate, CategoriaOut
from utils.db import db

async def create_categoria(categoria: CategoriaCreate):
    if await db["categorias"].find_one({"nombre": categoria.nombre}):
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    result = await db["categorias"].insert_one(categoria.dict())
    return await db["categorias"].find_one({"_id": result.inserted_id})
