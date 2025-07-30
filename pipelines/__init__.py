from .inventory import (
    pipeline_inventory_with_part
)

from .vehicle_parts import (
    pipeline_parts_by_vehicle,
    pipeline_vehicles_by_part
)

__all__ = [
    # Pipelines de inventario
    "pipeline_inventory_with_part",

    # Pipelines de compatibilidad vehículo-parte
    "pipeline_parts_by_vehicle",
    "pipeline_vehicles_by_part"
]
