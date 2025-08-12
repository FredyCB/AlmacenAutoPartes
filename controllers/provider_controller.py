from models.provider import Provider
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

providers_coll = get_collection("providers")

async def create_provider(provider: Provider) -> Provider:
    try:
        provider_dict = provider.model_dump(exclude={"id"})
        inserted = providers_coll.insert_one(provider_dict)
        provider.id = str(inserted.inserted_id)
        return provider
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating provider: {str(e)}")

async def get_providers() -> list[Provider]:
    try:
        providers = []
        for doc in providers_coll.find():
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            providers.append(Provider(**doc))
        return providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching providers: {str(e)}")


async def update_provider(provider_id: str, provider: Provider) -> dict:
    try:
        if not ObjectId.is_valid(provider_id):
            raise HTTPException(status_code=400, detail="Invalid provider ID")

        result = providers_coll.update_one(
            {"_id": ObjectId(provider_id)},
            {"$set": provider.model_dump(exclude={"id"})}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Provider not found")
        return {"message": "Provider updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating provider: {str(e)}")
