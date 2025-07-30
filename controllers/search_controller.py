from utils.mongodb import get_collection
from fastapi import HTTPException

parts_coll = get_collection("parts")

async def search_parts_by_name_or_description(query: str) -> list[dict]:
    try:
        regex = {"$regex": query, "$options": "i"}
        results = parts_coll.find({"$or": [{"name": regex}, {"description": regex}]})
        parts = []
        for part in results:
            part["id"] = str(part["_id"])
            del part["_id"]
            parts.append(part)
        return parts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in search: {str(e)}")