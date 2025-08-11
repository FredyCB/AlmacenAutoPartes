from fastapi import APIRouter, Request
from models.user import User
from models.login import Login
from controllers.users_controller import create_user, login

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
async def signup(user: User):
    return await create_user(user)

@router.post("/login")
async def signin(data: Login):
    return await login(data)
