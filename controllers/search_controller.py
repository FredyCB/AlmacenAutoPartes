from fastapi import HTTPException
from utils.mongodb import get_collection

CATALOG = "catalog"

def search_parts_by_name_or_description(query: str, skip: int = 0, limit: int = 20):
    coll = get_collection(CATALOG)
    regex = {"$regex": query, "$options": "i"}
    cursor = coll.find({"$or": [{"name": regex}, {"description": regex}], "active": True}).skip(skip).limit(limit)
    results = []
    for r in cursor:
        r["id"] = str(r["_id"]); del r["_id"]
        results.append(r)
    return results

def cross_reference_search(ref: str):
    coll = get_collection(CATALOG)
    results = list(coll.find({"cross_reference": ref}))
    if not results:
        raise HTTPException(status_code=404, detail="No matches")
    for r in results:
        r["id"] = str(r["_id"]); del r["_id"]
    return results
