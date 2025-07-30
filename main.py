import uvicorn
import logging

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

from controllers.users_controller import create_user, login
from models.user import User
from models.login import Login

# Routers
from routes.search_routes import router as search_routes_router
from routes.inventory_routes import router as inventory_routes_router
from routes.parts_routes import router as parts_routes_router
from routes.orders_routes import router as orders_routes_router
from routes.provider_routes import router as provider_routes_router
from routes.vehicle_routes import router as vehicle_routes_router


app = FastAPI(
    title="Autopartes API",
    version="1.0.0",
    description="API para la gestión de un almacén de autopartes",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    openapi_tags=[
        {"name": "Users", "description": "Gestión de usuarios y autenticación"},
        {"name": "Parts", "description": "Gestión de repuestos"},
        {"name": "Inventory", "description": "Gestión del inventario"},
        {"name": "Orders", "description": "Gestión de órdenes y reservas"},
        {"name": "Search", "description": "Búsqueda de repuestos"},
        {"name": "Providers", "description": "Gestión de proveedores"},
        {"name": "Vehicles", "description": "Gestión de vehículos"},
    ]
)

# Configuración global para que aparezca el botón Authorize
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API para el Almacén de Autopartes",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" not in method:
                method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Uso de los routers en la app
app.include_router(inventory_routes_router)
app.include_router(search_routes_router)
app.include_router(parts_routes_router)
app.include_router(orders_routes_router)
app.include_router(provider_routes_router)
app.include_router(vehicle_routes_router)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta base para crea usuario
@app.post("/users", tags=["Users"])
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

# Ruta base logear un usuario/admin
@app.post("/users/login", tags=["Users"])
async def login_access(l: Login) -> dict:
    return await login(l)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
