# Importamos FastAPI para crear la aplicación
from fastapi import FastAPI

# Importamos el router donde está el webhook de WhatsApp
from app.routers.webhook_router import router as webhook_router


# Creamos la aplicación principal de FastAPI
app = FastAPI(
    title="Lordart WhatsApp Bot",
    description="Bot de WhatsApp para responder clientes, mostrar catálogo y promociones.",
    version="1.0.0",
)


# Registramos el router del webhook
# Esto habilita las rutas:
# GET /webhook
# POST /webhook
app.include_router(webhook_router)


@app.get("/")
async def health_check():
    """
    Endpoint de prueba para saber si la API está corriendo.

    Puedes abrir:
    http://localhost:3000

    Y debe responder que el bot está funcionando.
    """

    return {
        "status": "ok",
        "message": "Lordart WhatsApp Bot funcionando correctamente",
    }