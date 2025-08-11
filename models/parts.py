from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional
from models.provider import ProviderOut

class PartBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str
    provider_id: str

    @validator('provider_id')
    def validate_provider_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID de proveedor inválido")
        return v

    @validator('price')
    def round_price(cls, v):
        return round(v, 2)

class PartWithProvider(PartOut):
    provider_info: ProviderOut
