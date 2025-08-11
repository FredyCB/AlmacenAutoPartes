from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from models.proveedor import Proveedor

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class PartCreate(BaseModel):
    nombre: str = Field(..., min_length=3)
    descripcion: str
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str
    proveedor_id: str

class Part(PartCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creado_por: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}

class PartWithProvider(Part):
    proveedor_info: Proveedor
