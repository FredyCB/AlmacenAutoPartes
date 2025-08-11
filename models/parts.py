from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId
from models.proveedor_model import ProveedorOut

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class PartIn(BaseModel):
    nombre: str = Field(..., min_length=3)
    descripcion: str
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str
    proveedor_id: str

    @validator('proveedor_id')
    def validate_proveedor_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID de proveedor inválido")
        return v

class PartOut(PartIn):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creado_por: str
    fecha_creacion: datetime

    class Config:
        json_encoders = {ObjectId: str}

class PartWithProveedor(PartOut):
    proveedor_info: ProveedorOut
