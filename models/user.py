from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class User(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=2)
    lastname: str = Field(min_length=2)
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", description="Correo electrónico del usuario")
    active: bool = True
    admin: bool = False
    password: str = Field(..., min_length=8, max_length=64)

    @validator("password")
    def password_complexity(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un dígito")
        return v
