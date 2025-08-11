import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Falta la variable de entorno SECRET_KEY")

security = HTTPBearer()

def create_jwt_token(firstname, lastname, email, active, admin, user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "id": str(user_id),
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "active": active,
        "admin": admin,
        "exp": int(expiration.timestamp()),
        "iat": int(datetime.utcnow().timestamp())
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def _get_request_from_args(*args, **kwargs):
    from fastapi import Request
    req = next((a for a in args if isinstance(a, Request)), None)
    if not req:
        req = kwargs.get("request")
    return req

def validateuser(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = _get_request_from_args(*args, **kwargs)
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid auth scheme")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if not payload.get("email") or not payload.get("active"):
                raise HTTPException(status_code=401, detail="Invalid token or inactive user")
            # check exp (numeric)
            if int(payload.get("exp",0)) < int(datetime.utcnow().timestamp()):
                raise HTTPException(status_code=401, detail="Expired token")
            request.state.id = payload.get("id")
            request.state.email = payload.get("email")
            request.state.firstname = payload.get("firstname")
            request.state.lastname = payload.get("lastname")
            request.state.admin = payload.get("admin", False)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await func(*args, **kwargs)
    return wrapper

def validateadmin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = _get_request_from_args(*args, **kwargs)
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid auth scheme")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Authorization header")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if not payload.get("email") or not payload.get("active") or not payload.get("admin"):
                raise HTTPException(status_code=401, detail="No autorizado")
            if int(payload.get("exp",0)) < int(datetime.utcnow().timestamp()):
                raise HTTPException(status_code=401, detail="Expired token")
            request.state.id = payload.get("id")
            request.state.email = payload.get("email")
            request.state.firstname = payload.get("firstname")
            request.state.lastname = payload.get("lastname")
            request.state.admin = True
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await func(*args, **kwargs)
    return wrapper
