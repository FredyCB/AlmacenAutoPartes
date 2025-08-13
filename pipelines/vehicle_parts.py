# pipelines/vehicle_parts.py
def parts_by_vehicle_pipeline(vehicle_id: str):
    return [
        {"$match": {"vehicle_id": vehicle_id}},
        {
            "$lookup": {
                "from": "catalog",
                "localField": "part_id",
                "foreignField": "_id",
                "as": "part"
            }
        },
        {"$unwind": {"path": "$part", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "vehicle_id": 1,
                "part_id": 1,
                "notes": 1,
                "part.name": 1,
                "part.description": 1,
                "part.price": 1
            }
        }
    ]

def vehicles_by_part_pipeline(part_id: str):
    return [
        {"$match": {"part_id": part_id}},
        {
            "$lookup": {
                "from": "vehicles",
                "localField": "vehicle_id",
                "foreignField": "_id",
                "as": "vehicle"
            }
        },
        {"$unwind": {"path": "$vehicle", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "vehicle_id": 1,
                "part_id": 1,
                "notes": 1,
                "vehicle.brand": 1,
                "vehicle.model": 1,
                "vehicle.year": 1
            }
        }
    ]

