from fastapi import APIRouter, Request
from models.user import User
from models.login import Login
from controllers.users_controller import create_user, login

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=dict)
async def create_user_endpoint(user: User):
    # ignore any admin field client may send: controller enforces admin=False
    return await create_user(user)

@router.post("/login", response_model=dict)
async def login_endpoint(payload: Login):
    return await login(payload)
