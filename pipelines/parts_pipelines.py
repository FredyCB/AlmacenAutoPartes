from bson import ObjectId
from typing import Optional

# Pipeline 1: Lookup (Parts + Proveedores)
def pipeline_parts_proveedor():
    return [
        {
            "$lookup": {
                "from": "proveedores",
                "localField": "proveedor_id",
                "foreignField": "_id",
                "as": "proveedor_info"
            }
        },
        {"$unwind": "$proveedor_info"},
        {"$project": {"proveedor_info.password": 0}}
    ]

# Pipeline 2: Cálculos estadísticos
def pipeline_estadisticas():
    return [
        {
            "$group": {
                "_id": "$categoria",
                "total_parts": {"$sum": 1},
                "precio_promedio": {"$avg": "$precio"},
                "stock_total": {"$sum": "$stock"},
                "valor_inventario": {"$sum": {"$multiply": ["$precio", "$stock"]}}
            }
        },
        {"$sort": {"_id": 1}}
    ]

# Pipeline 3: Validación para eliminar proveedor
def pipeline_validar_proveedor(proveedor_id: str):
    return [
        {
            "$match": {"proveedor_id": ObjectId(proveedor_id)}
        },
        {
            "$group": {
                "_id": None,
                "total_parts": {"$sum": 1},
                "parts": {"$push": "$nombre"}
            }
        }
    ]
