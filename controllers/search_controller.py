from utils.mongodb import get_collection
from fastapi import HTTPException

def search_parts(term: str, skip: int = 0, limit: int = 20):
    coll = get_collection("catalog")
    regex = {"$regex": term, "$options": "i"}
    docs = list(coll.find({"$and":[{"active":True},{"$or":[{"name":regex},{"description":regex}]}]}).skip(skip).limit(limit))
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs

def cross_reference_search(ref: str):
    coll = get_collection("catalog")
    docs = list(coll.find({"cross_reference": ref}))
    if not docs:
        raise HTTPException(status_code=404, detail="Not found")
    for d in docs:
        d["id"] = str(d["_id"])
        del d["_id"]
    return docs
