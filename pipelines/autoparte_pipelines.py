# Pipeline 1: Lookup (Autopartes + Proveedores)
pipeline_autoparte_proveedor = [
    {
        "$lookup": {
            "from": "proveedores",
            "localField": "proveedor_id",
            "foreignField": "_id",
            "as": "proveedor_info"
        }
    },
    {"$unwind": "$proveedor_info"}
]

# Pipeline 2: Cálculos (Agrupación por categoría)
pipeline_estadisticas = [
    {
        "$group": {
            "_id": "$categoria",
            "total": {"$sum": 1},
            "precio_promedio": {"$avg": "$precio"},
            "stock_total": {"$sum": "$stock"}
        }
    }
]

# Pipeline 3: Validación compleja (antes de eliminar proveedor)
pipeline_validar_proveedor = [
    {
        "$match": {"proveedor_id": ObjectId(proveedor_id)}
    },
    {
        "$group": {
            "_id": None,
            "total_autopartes": {"$sum": 1}
        }
    }
]
