import os
import logging
import requests
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from fastapi import HTTPException
from bson import ObjectId

from models.user import User
from models.login import Login
from utils.security import create_jwt_token
from utils.mongodb import get_collection

logger = logging.getLogger("users_controller")

# Initialize Firebase admin once
if not firebase_admin._apps:
    # expects secrets/autopartes-firebase.json to exist
    cred_path = os.path.join("secrets", "autopartes-firebase.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        logger.warning("No se encontró secrets/autopartes-firebase.json; operaciones Firebase fallarán si se requieren.")

USERS_COLL = "users"

async def create_user(user: User) -> dict:
    """
    Crea usuario: registra en Firebase Authentication y guarda user en MongoDB
    SIN guardar la contraseña en MongoDB.
    El campo admin no debe enviarse desde el cliente; se ignora en la creación.
    """
    try:
        # primero crear en Firebase
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
    except Exception as e:
        logger.warning(f"Firebase create_user error: {e}")
        raise HTTPException(status_code=400, detail="Error al registrar usuario en Firebase")

    try:
        coll = get_collection(USERS_COLL)
        new_user = {
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "active": True,
            "admin": False  # por defecto False, no se permite setear desde swagger
        }
        inserted = coll.insert_one(new_user)
        # respuesta: devolver usuario creado (sin password)
        return {
            "id": str(inserted.inserted_id),
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "active": True,
            "admin": False
        }
    except Exception as e:
        # rollback: eliminar usuario de Firebase
        try:
            firebase_auth.delete_user(user_record.uid)
        except Exception:
            pass
        logger.error(f"Error al guardar usuario en MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Error de base de datos")

async def login(user: Login) -> dict:
    """
    Loguea contra Firebase REST API para validar credenciales y luego emite un JWT propio
    con la info del usuario registrada en MongoDB (id, name, admin, active).
    """
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="FIREBASE_API_KEY no configurada")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": user.email,
        "password": user.password,
        "returnSecureToken": True
    }
    res = requests.post(url, json=payload)
    data = res.json()
    if "error" in data:
        raise HTTPException(status_code=400, detail="Credenciales inválidas (Firebase)")

    # obtener info del usuario desde MongoDB
    coll = get_collection(USERS_COLL)
    user_info = coll.find_one({"email": user.email})
    if not user_info:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    # preparar payload para JWT interno
    user_payload = {
        "id": str(user_info["_id"]),
        "firstname": user_info["name"],
        "lastname": user_info["lastname"],
        "email": user_info["email"],
        "active": user_info.get("active", True),
        "admin": user_info.get("admin", False)
    }
    token = create_jwt_token(user_payload)
    return {"message": "Autenticado", "idToken": token}
