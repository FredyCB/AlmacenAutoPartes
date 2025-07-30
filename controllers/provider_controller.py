from models.provider import Provider
from utils.mongodb import get_collection
from fastapi import HTTPException

providers_coll = get_collection("providers")

async def create_provider(provider: Provider) -> Provider:
    try:
        provider_dict = provider.model_dump(exclude={"id"})
        inserted = providers_coll.insert_one(provider_dict)
        provider.id = str(inserted.inserted_id)
        return provider
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating provider: {str(e)}")