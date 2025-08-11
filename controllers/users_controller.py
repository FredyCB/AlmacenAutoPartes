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

# Inicializar Firebase con credenciales en secrets/
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("secrets/autopartes-firebase.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        logger.warning("Firebase credentials not found or invalid: " + str(e))

async def create_user(user: User):
    # crear usuario en Firebase (autenticación)
    try:
        user_record = firebase_auth.create_user(email=user.email, password=user.password)
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=400, detail="Error al registrar usuario en Firebase")

    try:
        coll = get_collection("users")
        user_doc = {
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "active": True,
            "admin": False
        }
        result = coll.insert_one(user_doc)
        return {"message": "Usuario creado", "id": str(result.inserted_id)}
    except Exception as e:
        # si falla guardar en Mongo, eliminar usuario de Firebase
        try:
            firebase_auth.delete_user(user_record.uid)
        except Exception:
            pass
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error de base de datos")
    
async def login(user: Login):
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="FIREBASE_API_KEY no configurada")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": user.email, "password": user.password, "returnSecureToken": True}
    resp = requests.post(url, json=payload)
    data = resp.json()
    if "error" in data:
        raise HTTPException(status_code=400, detail="Error autenticación Firebase")
    # buscar usuario en Mongo
    coll = get_collection("users")
    user_info = coll.find_one({"email": user.email})
    if not user_info:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en MongoDB")
    token = create_jwt_token(user_info.get("name"), user_info.get("lastname"), user_info.get("email"), user_info.get("active", True), user_info.get("admin", False), str(user_info["_id"]))
    return {"message": "Autenticado", "idToken": token}
