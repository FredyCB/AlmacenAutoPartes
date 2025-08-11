# Añadir al inicio
from pipelines.autoparte_pipelines import *

# Nuevo método para endpoint con pipeline
async def get_autopartes_con_proveedor():
    return await db["autopartes"].aggregate(pipeline_autoparte_proveedor).to_list(None)

# Nuevo método para estadísticas
async def get_estadisticas_autopartes():
    return await db["autopartes"].aggregate(pipeline_estadisticas).to_list(None)
