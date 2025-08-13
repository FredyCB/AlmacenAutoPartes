from pydantic import BaseModel, Field
from typing import Optional

class Vehicle(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID generado automáticamente por MongoDB"
    )

    brand: str = Field(
        description="Marca del vehículo",
        examples=["Toyota", "Nissan", "Ford"]
    )

    model: str = Field(
        description="Modelo del vehículo",
        examples=["Corolla", "Sentra", "F-150"]
    )

    year: int = Field(
        description="Año del vehículo",
        ge=1900,
        le=2100,
        examples=[2020, 2018]
    )

    active: bool = Field(
        default=True,
        description="Indica si el modelo de vehículo está activo"
    )
