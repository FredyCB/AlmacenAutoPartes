import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

load_dotenv()

DB = os.getenv("DATABASE_NAME")
URI = os.getenv("MONGODB_URI")


def get_collection(col: str):
    """Devuelve una colección desde la base de datos MongoDB"""
    if not URI or not DB:
        raise ValueError("Faltan las variables de entorno MONGO_URI o MONGO_DB_NAME")

    client = MongoClient(
        URI,
        server_api=ServerApi("1"),
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    return client[DB][col]
