# httpx permite hacer peticiones HTTP asíncronas
import httpx

# Importamos la configuración del proyecto
from app.core.config import settings


class WhatsAppClient:
    """
    Esta clase se encarga únicamente de comunicarse con la API de WhatsApp Cloud.

    Aquí NO va la lógica del negocio.
    Aquí solo se envían mensajes hacia Meta:
    - Texto
    - Imágenes
    - Plantillas
    """

    def __init__(self):
        """
        Constructor de la clase.

        Aquí armamos:
        - URL base de la API de Meta
        - Headers con autorización
        """

        # URL oficial para enviar mensajes usando el Phone Number ID
        self.base_url = (
            f"https://graph.facebook.com/{settings.graph_api_version}/"
            f"{settings.phone_number_id}/messages"
        )

        # Headers necesarios para autenticar la petición
        self.headers = {
            "Authorization": f"Bearer {settings.whatsapp_token}",
            "Content-Type": "application/json",
        }

    async def send_text(self, to: str, message: str) -> dict:
        """
        Envía un mensaje de texto simple por WhatsApp.

        Parámetros:
        - to: número destino. Ejemplo: 573001234567
        - message: texto que se enviará al cliente
        """

        # Payload que exige WhatsApp Cloud API para enviar texto
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message,
            },
        }

        # Creamos un cliente HTTP asíncrono para enviar la petición
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )

        # Retornamos el estado y la respuesta de Meta
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
        }

    async def send_image_by_url(self, to: str, image_url: str, caption: str) -> dict:
        """
        Envía una imagen al cliente usando una URL pública.

        Importante:
        La imagen debe estar en internet.
        No sirve una ruta local como C:/imagenes/foto.jpg.
        """

        # Payload para enviar imagen con descripción
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {
                "link": image_url,
                "caption": caption,
            },
        }

        # Enviamos la petición a Meta
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )

        # Retornamos la respuesta para poder revisar errores si algo falla
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
        }

    async def send_template(
        self,
        to: str,
        template_name: str,
        language_code: str = "es",
    ) -> dict:
        """
        Envía una plantilla aprobada por Meta.

        Esto se usa cuando:
        - Quieres iniciar conversación con un cliente.
        - Quieres enviar promociones.
        - Ya pasaron más de 24 horas desde el último mensaje del cliente.

        La plantilla debe estar creada y aprobada en Meta.
        """

        # Payload para enviar una plantilla
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code,
                },
            },
        }

        # Enviamos la plantilla a través de la API
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )

        # Retornamos la respuesta de Meta
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
        }