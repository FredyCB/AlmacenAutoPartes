import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import jwt
from jwt import PyJWTError
from functools import wraps

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
security = HTTPBearer()

# ----------------------------
# Funciones Base
# ----------------------------

def create_jwt_token(user_data: dict, expires_delta: timedelta = None):
    """Crea token JWT con datos del usuario"""
    to_encode = user_data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "role": "admin" if user_data.get("admin") else "user"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    """Decodifica y valida token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
            
        return payload
        
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

# ----------------------------
# Dependencias FastAPI
# ----------------------------

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependencia para obtener usuario autenticado"""
    token = credentials.credentials
    payload = decode_jwt_token(token)
    
    if not payload.get("active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
        
    return payload

def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependencia para validar administradores"""
    token = credentials.credentials
    payload = decode_jwt_token(token)
    
    if not payload.get("admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador"
        )
        
    return payload

# ----------------------------
# Decoradores Legacy (compatibilidad)
# ----------------------------

def validateuser(func):
    """Decorador para endpoints que requieren autenticación"""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        credentials = await security(request)
        user_data = get_current_user(credentials)
        request.state.user = user_data
        return await func(request, *args, **kwargs)
    return wrapper

def validateadmin(func):
    """Decorador para endpoints de administrador"""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        credentials = await security(request)
        admin_data = get_admin_user(credentials)
        request.state.admin = admin_data
        return await func(request, *args, **kwargs)
    return wrapper
