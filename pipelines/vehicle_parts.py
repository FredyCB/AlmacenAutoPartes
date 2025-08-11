def parts_by_vehicle_pipeline(vehicle_id):
    return [
        {"$match":{"vehicle_id": vehicle_id}},
        {"$lookup":{"from":"catalog","localField":"part_id","foreignField":"_id","as":"part"}},
        {"$unwind":"$part"},
        {"$project":{"id":{"$toString":"$_id"},"part_id":1,"vehicle_id":1,"part.name":1,"part.price":1}}
    ]
