import json

from fastapi import APIRouter, Request, Response

from app.core.config import settings
from app.services.bot_service import BotService


router = APIRouter(tags=["WhatsApp Webhook"])
bot_service = BotService()


@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Meta usa este GET para verificar el webhook.
    Si el token coincide, devolvemos el challenge.
    """

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("Verificación webhook recibida:")
    print("mode:", mode)
    print("token:", token)
    print("challenge:", challenge)

    if mode == "subscribe" and token == settings.verify_token:
        return Response(content=challenge, media_type="text/plain")

    return Response(content="Token inválido", status_code=403)


@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Meta usa este POST para enviar mensajes entrantes.
    Aquí procesamos los mensajes de WhatsApp.
    """

    # Leemos el body crudo primero
    raw_body = await request.body()

    # Si llega vacío, no intentamos convertirlo a JSON
    if not raw_body:
        print("POST /webhook recibido sin body")
        return {
            "status": "empty_body",
            "message": "La petición llegó sin JSON"
        }

    # Intentamos convertir el body a JSON
    try:
        body = json.loads(raw_body)
    except json.JSONDecodeError as error:
        print("JSON inválido recibido:", raw_body)
        print("Error:", error)

        return {
            "status": "invalid_json",
            "message": "El body recibido no es un JSON válido"
        }

    print("Webhook recibido:", body)

    try:
        entries = body.get("entry", [])

        for entry in entries:
            changes = entry.get("changes", [])

            for change in changes:
                value = change.get("value", {})

                messages = value.get("messages", [])

                # Si no hay mensajes, puede ser un evento de estado.
                if not messages:
                    print("Webhook sin mensajes. Puede ser status/update.")
                    continue

                for message in messages:
                    phone = message.get("from")
                    message_type = message.get("type")

                    print("Tipo de mensaje:", message_type)
                    print("Número origen:", phone)

                    if message_type == "text":
                        text = message.get("text", {}).get("body", "")

                        print("Texto recibido:", text)

                        await bot_service.process_text_message(phone, text)

        return {"status": "ok"}

    except Exception as error:
        print("Error procesando webhook:", error)

        return {
            "status": "error",
            "detail": str(error)
        }