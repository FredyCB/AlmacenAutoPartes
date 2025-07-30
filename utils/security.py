import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

# Si no existe la clave secreta, se detiene la ejecución del proyecto
if not SECRET_KEY:
    raise ValueError("Falta la variable de entorno SECRET_KEY")

security = HTTPBearer()
# Funcion para crear los tokens

def create_jwt_token(firstname, lastname, email, active, admin, user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)

    # Información que contendrá el token
    payload = {
        "id": user_id,             # ID único del usuario (MongoDB _id)
        "firstname": firstname,    # Nombre del usuario
        "lastname": lastname,      # Apellido del usuario
        "email": email,            # Correo del usuario
        "active": active,          # Estado activo del usuario
        "admin": admin,            # Si el usuario es administrador
        "exp": expiration,         # Tiempo de expiración del token
        "iat": datetime.utcnow()   # Fecha y hora en que se emitió el token
    }

    # Se firma el token usando la clave secreta y el algoritmo HS256
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # type: ignore

# Decorador para validar usuarios regulares
def validateuser(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        # Se obtiene el objeto "request" de los argumentos de la función
        request = next((arg for arg in args if isinstance(arg, Request)), None)
        if not request:
            request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        # Se obtiene el header Authorization
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Falta el token de autorización")

        # Se espera el formato: "Bearer <token>"
        schema, token = auth.split()
        if schema.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema inválido")

        try:
            # Se decodifica el token usando la clave secreta
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore

            # Verificamos que tenga datos mínimos válidos
            if not payload.get("email") or not payload.get("active"):
                raise HTTPException(status_code=401, detail="Token inválido")

            # Verificamos que el token no esté expirado
            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expirado")

            # Guardamos la información del usuario para usarla en los endpoints
            request.state.id = payload["id"]
            request.state.email = payload["email"]
            request.state.firstname = payload["firstname"]
            request.state.lastname = payload["lastname"]
            request.state.admin = payload.get("admin", False)

        except jwt.ExpiredSignatureError:
            # Error cuando el token ha caducado
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.PyJWTError:
            # Error cuando el token no es válido
            raise HTTPException(status_code=401, detail="Token inválido")

        # Si todo está bien, ejecuta la función original
        return await func(*args, **kwargs)
    return wrapper

# Decorador para validar tokens de admins

def validateadmin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        # Se obtiene el objeto "request"
        request = next((arg for arg in args if isinstance(arg, Request)), None)
        if not request:
            request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        # Se obtiene el token del header Authorization
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Falta el token de autorización")

        schema, token = auth.split()
        if schema.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Esquema inválido")

        try:
            # Se decodifica el token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore

            # Se verifica que sea admin y que esté activo
            if not payload.get("email") or not payload.get("admin") or not payload.get("active"):
                raise HTTPException(status_code=401, detail="No autorizado")

            # Verificamos expiración
            if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expirado")

            # Guardamos la info en request para otros endpoints
            request.state.id = payload["id"]
            request.state.email = payload["email"]
            request.state.firstname = payload["firstname"]
            request.state.lastname = payload["lastname"]
            request.state.admin = True

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Ejecuta la función original si pasa la validacion
        return await func(*args, **kwargs)
    return wrapper
