# pipelines/inventory.py
def inventory_with_parts_pipeline(skip: int = 0, limit: int = 100):
    # Une inventory con catalog (colección 'catalog' o 'parts')
    return [
        {
            "$lookup": {
                "from": "catalog",
                "localField": "part_id",
                "foreignField": "_id",
                "as": "part"
            }
        },
        {"$unwind": {"path": "$part", "preserveNullAndEmptyArrays": True}},
        {"$skip": skip},
        {"$limit": limit},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "part_id": 1,
                "quantity": 1,
                "provider_id": 1,
                "location": 1,
                "part.name": 1,
                "part.description": 1,
                "part.price": 1
            }
        }
    ]
