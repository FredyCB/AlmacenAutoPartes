import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from functools import wraps
from dotenv import load_dotenv
import json
import firebase_admin
from firebase_admin import credentials

# Cargamos el JSON desde la variable de entorno
firebase_config_json = os.environ.get("FIREBASE_CONFIG")
if not firebase_config_json:
    raise RuntimeError("FIREBASE_CONFIG environment variable not set")

firebase_config = json.loads(firebase_config_json)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("Falta la variable de entorno SECRET_KEY")

security = HTTPBearer()


def create_jwt_token(firstname, lastname, email, active, admin, user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "id": user_id,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "active": active,
        "admin": admin,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256") # type: ignore


def validateuser(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = next((arg for arg in args if isinstance(arg, Request)), None)
        if not request:
            request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Falta el token de autorización")

        schema, token = auth.split()
        if schema.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema inválido")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # type: ignore

            if not payload.get("email") or not payload.get("active"):
                raise HTTPException(status_code=401, detail="Token inválido")

            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expirado")

            request.state.id = payload["id"]
            request.state.email = payload["email"]
            request.state.firstname = payload["firstname"]
            request.state.lastname = payload["lastname"]
            request.state.admin = payload.get("admin", False)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        return await func(*args, **kwargs)
    return wrapper


def validateadmin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = next((arg for arg in args if isinstance(arg, Request)), None)
        if not request:
            request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Falta el token de autorización")

        schema, token = auth.split()
        if schema.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema inválido")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # type: ignore

            if not payload.get("email") or not payload.get("admin") or not payload.get("active"):
                raise HTTPException(status_code=401, detail="No autorizado")

            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expirado")

            request.state.id = payload["id"]
            request.state.email = payload["email"]
            request.state.firstname = payload["firstname"]
            request.state.lastname = payload["lastname"]
            request.state.admin = True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        return await func(*args, **kwargs)
    return wrapper

