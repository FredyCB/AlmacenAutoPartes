from pydantic import BaseModel, Field
from typing import Optional

class Provider(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID generado automáticamente por MongoDB"
    )

    name: str = Field(
        description="Nombre del proveedor",
        min_length=1,
        max_length=100,
        examples=["Bosch", "Toyota", "ACME Autopartes"]
    )

    contact_email: str = Field(
        description="Correo electrónico de contacto",
        examples=["ventas@proveedor.com"]
    )

    phone: str = Field(
        description="Teléfono de contacto",
        examples=["+50412345678"]
    )

    active: bool = Field(
        default=True,
        description="Indica si el proveedor está activo"
    )
