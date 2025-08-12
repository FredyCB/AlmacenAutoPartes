def pipeline_parts_by_vehicle(vehicle_id: str):
    """
    Obtener autopartes compatibles con un vehículo específico.
    """
    return [
        { "$match": { "id_vehicle": vehicle_id } },
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
                "id_vehicle": 1,
                "notes": 1,
                "part.name": 1,
                "part.description": 1,
                "part.cost": 1,
                "part.discount": 1
            }
        }
    ]

def pipeline_vehicles_by_part(part_id: str):
    """
    Obtener vehículos compatibles con una autoparte específica.
    """
    return [
        { "$match": { "id_part": part_id } },
        {
            "$lookup": {
                "from": "vehicle",
                "localField": "id_vehicle",
                "foreignField": "_id",
                "as": "vehicle"
            }
        },
        { "$unwind": "$vehicle" },
        {
            "$project": {
                "id": { "$toString": "$_id" },
                "id_vehicle": 1,
                "id_part": 1,
                "notes": 1,
                "vehicle.brand": 1,
                "vehicle.model": 1,
                "vehicle.year": 1
            }
        }
    ]
