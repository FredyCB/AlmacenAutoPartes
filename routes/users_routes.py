from fastapi import APIRouter
from models.user import User
from models.login import Login
from controllers.users_controller import create_user, login

# El prefijo se mantiene en /users
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=dict)
async def create_user_endpoint(user: User):
    """
    Crea un nuevo usuario.
    Este endpoint es el básico: POST /users
    """
    return await create_user(user)

@router.post("/register", response_model=dict)
async def register_endpoint(user: User):
    """
    Endpoint de registro que el frontend espera: POST /users/register
    """
    return await create_user(user)

@router.post("/login", response_model=dict)
async def login_endpoint(payload: Login):
    """
    Login de usuario: POST /users/login
    """
    return await login(payload)
