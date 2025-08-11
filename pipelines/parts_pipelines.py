from bson import ObjectId
from typing import Optional

# Pipeline 1: Lookup (Parts + Proveedores) - EXISTENTE (mejorado)
def parts_with_providers():
    return [
        {
            "$lookup": {
                "from": "providers",
                "localField": "provider_id",
                "foreignField": "_id",
                "as": "provider_info"
            }
        },
        {"$unwind": "$provider_info"},
        {"$project": {"provider_info.password": 0}}  # Excluir datos sensibles
    ]

# Pipeline 2: Cálculos estadísticos - NUEVO (completo)
def parts_statistics():
    return [
        {
            "$group": {
                "_id": "$category",
                "total_parts": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "total_stock": {"$sum": "$stock"},
                "inventory_value": {"$sum": {"$multiply": ["$price", "$stock"]}}
            }
        },
        {"$sort": {"_id": 1}}
    ]

# Pipeline 3: Validación compleja - NUEVO
def validate_provider_usage(provider_id: str):
    return [
        {"$match": {"provider_id": ObjectId(provider_id)}},
        {
            "$group": {
                "_id": None,
                "total_parts": {"$sum": 1},
                "parts_list": {"$push": "$name"}
            }
        }
    ]

# Pipeline 4: Búsqueda avanzada - NUEVO
def search_pipeline(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    match_stage = {}
    if category:
        match_stage["category"] = category
    if min_price or max_price:
        match_stage["price"] = {}
        if min_price:
            match_stage["price"]["$gte"] = min_price
        if max_price:
            match_stage["price"]["$lte"] = max_price
    
    return [{"$match": match_stage}] if match_stage else []
