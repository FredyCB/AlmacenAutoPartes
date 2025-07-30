from fastapi import APIRouter
from models.user import User
from models.login import Login
from controllers.users_controller import create_user, login

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
async def create_user_endpoint(user: User):
    """Registrar un nuevo usuario (por defecto admin=False)."""
    return await create_user(user)

@router.post("/login", response_model=dict)
async def login_endpoint(l: Login):
    """Iniciar sesión y obtener un JWT válido."""
    return await login(l)
