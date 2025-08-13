import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users_routes import router as users_router
from routes.parts_routes import router as parts_router
from routes.inventory_routes import router as inventory_router
from routes.orders_routes import router as orders_router
from routes.provider_routes import router as providers_router
from routes.search_routes import router as search_router
from routes.vehicles_routes import router as vehicles_router
from routes.vehicle_parts_routes import router as vehicle_parts_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Almacen Autopartes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod restringir a tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(users_router)
app.include_router(parts_router)
app.include_router(inventory_router)
app.include_router(orders_router)
app.include_router(providers_router)
app.include_router(search_router)
app.include_router(vehicles_router)
app.include_router(vehicle_parts_router)

@app.get("/")
def root():
    return {"message": "Almacén Autopartes API - OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)