from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional
from datetime import datetime
from models.provider import ProviderOut

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ObjectId inválido")
        return ObjectId(v)

class PartBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Bomba de aceite")
    description: str = Field(..., min_length=10, example="Bomba de aceite para motor 2.0L")
    price: float = Field(..., gt=0, example=125.99)
    stock: int = Field(..., ge=0, example=15)
    category: str = Field(..., example="motor")
    provider_id: str = Field(..., example="507f1f77bcf86cd799439011")

    @validator('provider_id')
    def validate_provider_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID de proveedor inválido")
        return v

    @validator('price')
    def round_price(cls, v):
        return round(v, 2)

class PartCreate(PartBase):
    pass

class PartOut(PartBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439012",
                "name": "Bomba de aceite",
                "price": 125.99,
                "stock": 15,
                "category": "motor",
                "created_by": "user@example.com",
                "created_at": "2023-01-01T00:00:00"
            }
        }

class PartWithProvider(PartOut):
    provider_info: ProviderOut
