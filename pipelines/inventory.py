def inventory_with_parts_pipeline():
    return [
        {
            "$lookup": {
                "from": "catalog",
                "localField": "part_id",
                "foreignField": "_id",
                "as": "part"
            }
        },
        {"$unwind": {"path":"$part","preserveNullAndEmptyArrays": True}},
        {"$project": {"id":{"$toString":"$_id"},"part_id":1,"quantity":1,"location":1,"part.name":1,"part.price":1,"part.description":1}}
    ]
