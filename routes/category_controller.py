from fastapi import HTTPException
from bson import ObjectId
from models.category import Category
from utils.mongodb import get_collection

categories_coll = get_collection("categories")

async def create_category(category: Category) -> Category:
    try:
        category_dict = category.model_dump(exclude={"id"})
        result = categories_coll.insert_one(category_dict)
        category.id = str(result.inserted_id)
        return category
    except Exception as e:
        raise HTTPException(500, f"Error creating category: {e}")

async def get_category_by_id(category_id: str) -> Category:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(400, "Invalid ID format")
    category = categories_coll.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(404, "Category not found")
    category["id"] = str(category["_id"])
    del category["_id"]
    return category

async def get_all_categories() -> list[Category]:
    categories = []
    for category in categories_coll.find():
        category["id"] = str(category["_id"])
        del category["_id"]
        categories.append(category)
    return categories

async def update_category(category_id: str, data: dict) -> dict:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(400, "Invalid ID format")
    result = categories_coll.update_one({"_id": ObjectId(category_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(404, "Category not found")
    return {"message": "Category updated successfully"}

async def delete_category(category_id: str) -> dict:
    if not ObjectId.is_valid(category_id):
        raise HTTPException(400, "Invalid ID format")
    result = categories_coll.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Category not found")
    return {"message": "Category deleted successfully"}
