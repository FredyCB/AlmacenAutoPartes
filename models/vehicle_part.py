from pydantic import BaseModel, Field
from typing import Optional

class VehiclePart(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID generado automáticamente por MongoDB"
    )

    id_vehicle: str = Field(
        description="ID del vehículo compatible"
    )

    id_part: str = Field(
        description="ID de la autoparte (catalog)"
    )

    notes: Optional[str] = Field(
        default=None,
        description="Notas opcionales sobre la compatibilidad",
        examples=["Solo para versiones con motor 2.0L"]
    )
