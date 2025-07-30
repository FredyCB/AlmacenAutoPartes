import os
import logging
import firebase_admin
import requests
from fastapi import HTTPException
from firebase_admin import credentials, auth as firebase_auth
from models.user import User
from models.login import Login
from utils.security import create_jwt_token
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("secrets/autopartes-firebase.json")
    firebase_admin.initialize_app(cred)

async def create_user(user: User) -> User:
    
    #Crea un usuario en Firebase y lo registra en MongoDB.

    try:
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=400, detail="Error al registrar usuario en Firebase")

    try:
        coll = get_collection("users")
        new_user = {
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "active": True,
            "admin": False  # Se fuerza a False por defecto
        }

        inserted = coll.insert_one(new_user)

        return User(
            id=str(inserted.inserted_id),
            name=user.name,
            lastname=user.lastname,
            email=user.email,
            active=True,
            password="*********"
        )

    except Exception as e:
        firebase_auth.delete_user(user_record.uid)
        logger.error(f"Error al guardar usuario en MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")

async def login(user: Login) -> dict:
    
    #Autenticación de usuario mediante Firebase + generación de JWT.
    api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": user.email,
        "password": user.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if "error" in data:
        raise HTTPException(status_code=400, detail="Error al autenticar con Firebase")

    coll = get_collection("users")
    user_info = coll.find_one({"email": user.email})
    if not user_info:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en MongoDB")

    jwt_token = create_jwt_token(
        firstname=user_info["name"],
        lastname=user_info["lastname"],
        email=user_info["email"],
        active=user_info["active"],
        admin=user_info["admin"],
        user_id=str(user_info["_id"])
    )

    return {
        "message": "Usuario autenticado correctamente",
        "idToken": jwt_token
    }
