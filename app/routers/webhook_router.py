# Importamos herramientas de FastAPI para crear rutas
from fastapi import APIRouter, Request, Response

# Importamos la configuración del proyecto
from app.core.config import settings

# Importamos el servicio principal del bot
from app.services.bot_service import BotService


# Creamos un router para agrupar endpoints relacionados con WhatsApp
router = APIRouter(tags=["WhatsApp Webhook"])

# Creamos una instancia del bot
bot_service = BotService()


@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Endpoint GET usado por Meta para verificar el webhook.

    Cuando configuras en Meta:
    - URL de devolución de llamada
    - Verify token

    Meta llama esta ruta con:
    - hub.mode
    - hub.verify_token
    - hub.challenge

    Si el token coincide, debemos devolver el challenge.
    """

    # Obtenemos los parámetros enviados por Meta
    params = request.query_params

    # Modo de verificación enviado por Meta
    mode = params.get("hub.mode")

    # Token que Meta nos devuelve para comparar
    token = params.get("hub.verify_token")

    # Challenge que debemos retornar si todo está bien
    challenge = params.get("hub.challenge")

    # Validamos que el modo sea subscribe y que el token coincida con el .env
    if mode == "subscribe" and token == settings.verify_token:
        return Response(content=challenge, media_type="text/plain")

    # Si el token no coincide, rechazamos la verificación
    return Response(content="Token inválido", status_code=403)


@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Endpoint POST usado por Meta para enviar eventos.

    Aquí llegan:
    - Mensajes entrantes
    - Estados de mensajes
    - Otros eventos relacionados con WhatsApp

    En este caso procesamos mensajes de texto.
    """

    # Leemos el cuerpo JSON que envía Meta
    body = await request.json()

    # Imprimimos el JSON para depuración local
    print("Webhook recibido:", body)

    try:
        # Meta puede enviar varias entradas en el mismo webhook
        entries = body.get("entry", [])

        # Recorremos cada entrada
        for entry in entries:
            changes = entry.get("changes", [])

            # Recorremos cada cambio dentro de la entrada
            for change in changes:
                value = change.get("value", {})

                # Obtenemos mensajes entrantes
                messages = value.get("messages", [])

                # Recorremos cada mensaje recibido
                for message in messages:
                    # Número del cliente que escribió
                    phone = message.get("from")

                    # Tipo de mensaje: text, image, audio, etc.
                    message_type = message.get("type")

                    # Por ahora solo procesamos mensajes de texto
                    if message_type == "text":
                        text = message.get("text", {}).get("body", "")

                        # Enviamos el mensaje al servicio del bot
                        await bot_service.process_text_message(phone, text)

        # Respuesta exitosa para que Meta sepa que recibimos el evento
        return {"status": "ok"}

    except Exception as error:
        # Si algo falla, imprimimos el error
        print("Error procesando webhook:", error)

        # Retornamos el error en formato JSON
        return {
            "status": "error",
            "detail": str(error),
        }