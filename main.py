import uvicorn
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from controllers.users_controller import create_user, login
from models.user import User
from models.login import Login

from utils.security import validateuser, validateadmin

# Importación de todos los routers


# Routers para el almacén de autopartes:
from routes.search_routes import router as search_routes_router
from routes.provider_routes import router as providers_router
from routes.vehicles_routes import router as vehicles_router
from routes.vehicle_parts_routes import router as vehicle_parts_router
from routes.inventory_routes import router as inventory_routes_router
from routes.parts_routes import router as parts_routes_router
from routes.provider_routes import router as provider_routes_router
from routes.vehicles_routes import router as vehicle_routes_router
from routes.category_routes import router as category_routes_router


app = FastAPI(title="Autopartes API", version="1.0.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers nuevos
app.include_router(providers_router)
app.include_router(vehicles_router)
app.include_router(vehicle_parts_router)
app.include_router(inventory_routes_router)
app.include_router(search_routes_router)
app.include_router(parts_routes_router)
app.include_router(provider_routes_router)
app.include_router(vehicle_routes_router)
app.include_router(category_routes_router)


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rutas base
@app.get("/")
def read_root():
    return {"version": "1.0.0", "message": "API del Almacén de Autopartes"}

@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
@validateuser
@validateadmin
async def login_access(l: Login) -> dict:
    return await login(l)

# Correr servidor localmente
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
