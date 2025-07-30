from fastapi import HTTPException
from bson import ObjectId
from models.inventory import Inventory
from utils.mongodb import get_collection

#Creacion de la coleccion del inventario
inventory_coll = get_collection("inventory")

#funcion para agregar inventario
async def add_inventory(item: Inventory) -> Inventory:
    item_dict = item.model_dump(exclude={"id"})
    inserted = inventory_coll.insert_one(item_dict)
    item.id = str(inserted.inserted_id)
    return item

#funcion para consultar una parte o pieza del inventario
async def get_inventory_by_part(part_id: str) -> list:
    return list(inventory_coll.find({"id_part": part_id}))

#funcion para actualizar estado del inventario
async def update_stock(inventory_id: str, quantity: int) -> dict:
    if not ObjectId.is_valid(inventory_id):
        raise HTTPException(400, "Invalid ID")
    result = inventory_coll.update_one({"_id": ObjectId(inventory_id)}, {"$set": {"stock": quantity}})
    if result.matched_count == 0:
        raise HTTPException(404, "Inventory item not found")
    return {"message": "Stock updated"}

#funcion de alerta para stock bajo en inventario
async def get_low_stock_items() -> list:
    return list(inventory_coll.find({"stock": {"$lt": 10}}))
