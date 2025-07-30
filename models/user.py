from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class UserCreate(BaseModel):
    """
    Modelo para crear usuario (sin campos admin ni active).
    """
    name: str = Field(pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
    lastname: str = Field(pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(min_length=8, max_length=64)

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str):
        if not re.search(r"[A-Z]", value): raise ValueError("Debe tener una mayúscula.")
        if not re.search(r"\d", value): raise ValueError("Debe tener un número.")
        if not re.search(r"[@$!%*?&]", value): raise ValueError("Debe tener un caracter especial.")
        return value


class User(BaseModel):
    """
    Modelo general del usuario (para consultas/respuestas).
    """
    id: Optional[str] = Field(default=None)
    name: str
    lastname: str
    email: str
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    password: Optional[str] = Field(default="*********")
