from pydantic import BaseModel, Field

class Login(BaseModel):
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="Correo del usuario")
    password: str = Field(..., min_length=8)
