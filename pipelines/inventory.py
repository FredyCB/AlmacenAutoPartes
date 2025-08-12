def pipeline_inventory_with_part():
    """
    Pipeline para unir inventario con información de autoparte (Catalog).
    """
    return [
        {
            "$lookup": {
                "from": "catalog",
                "localField": "id_part",
                "foreignField": "_id",
                "as": "part"
            }
        },
        { "$unwind": "$part" },
        {
            "$project": {
                "id": { "$toString": "$_id" },
                "id_part": 1,
                "quantity": 1,
                "minimum_stock": 1,
                "location": 1,
                "active": 1,
                "part.name": 1,
                "part.cost": 1,
                "part.description": 1,
                "part.discount": 1
            }
        }
    ]
