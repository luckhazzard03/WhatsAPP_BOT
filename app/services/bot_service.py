# Importamos la configuración para obtener datos como el número administrador
from app.core.config import settings

# Cliente que envía mensajes usando WhatsApp Cloud API
from app.services.whatsapp_client import WhatsAppClient

# Servicio que construye mensajes de catálogo y promociones
from app.services.catalog_service import CatalogService

# Servicio que genera textos para el canal de WhatsApp
from app.services.channel_post_service import ChannelPostService


class BotService:
    """
    Servicio principal del bot.

    Este servicio recibe:
    - El número del cliente
    - El texto que escribió

    Y decide qué respuesta enviar.
    """

    def __init__(self):
        """
        Constructor del bot.

        Aquí inicializamos los servicios que el bot necesita.
        """

        # Cliente para enviar mensajes a WhatsApp
        self.whatsapp_client = WhatsAppClient()

        # Servicio para consultar catálogo y promociones
        self.catalog_service = CatalogService()

        # Servicio para generar publicaciones del canal
        self.channel_post_service = ChannelPostService()

    async def process_text_message(self, phone: str, text: str) -> dict:
        """
        Procesa el mensaje de texto recibido desde WhatsApp.

        Parámetros:
        - phone: número del cliente que escribió
        - text: mensaje enviado por el cliente
        """

        # Normalizamos el texto para comparar fácil
        clean_text = text.lower().strip()

        # Saludo inicial
        if clean_text in ["hola", "buenas", "buenos dias", "buenos días", "buenas tardes"]:
            return await self.send_welcome(phone)

        # Opción 1: catálogo
        if clean_text in ["1", "catalogo", "catálogo", "ver catalogo", "ver catálogo"]:
            return await self.send_catalog(phone)

        # Opción 2: promociones
        if clean_text in ["2", "promo", "promos", "promociones", "promoción"]:
            return await self.send_promotions(phone)

        # Opción 3: regalos
        if clean_text in ["3", "regalo", "detalles", "detalle"]:
            return await self.send_gift_options(phone)

        # Opción 4: atención humana
        if clean_text in ["4", "asesor", "humano", "persona"]:
            return await self.send_human_support(phone)

        # Opción 5: canal
        if clean_text in ["5", "canal", "novedades"]:
            return await self.send_channel_link(phone)

        # Comando interno para generar publicación del canal
        if clean_text in ["publicacion", "publicación", "post canal"]:
            return await self.send_channel_post_to_admin(phone)

        # Si el usuario escribe un número, intentamos buscar producto por ID
        if clean_text.isdigit():
            return await self.send_product_detail(phone, int(clean_text))

        # Si no coincide con nada, enviamos ayuda
        return await self.send_default(phone)

    async def send_welcome(self, phone: str) -> dict:
        """
        Envía el mensaje de bienvenida con el menú principal.
        """

        message = (
            "Hola 👋 Bienvenido a Lordart Diseño y Creatividad.\n\n"
            "Creamos detalles personalizados, cuadros, agendas en madera, "
            "llaveros, portacelulares y regalos especiales.\n\n"
            "Escribe una opción:\n\n"
            "1. Ver catálogo\n"
            "2. Ver promociones\n"
            "3. Detalles para regalo\n"
            "4. Hablar con una persona\n"
            "5. Ver canal de novedades"
        )

        return await self.whatsapp_client.send_text(phone, message)

    async def send_catalog(self, phone: str) -> dict:
        """
        Envía el catálogo completo al cliente.
        """

        # Construimos el mensaje usando CatalogService
        message = self.catalog_service.build_catalog_message()

        # Enviamos el mensaje por WhatsApp
        return await self.whatsapp_client.send_text(phone, message)

    async def send_promotions(self, phone: str) -> dict:
        """
        Envía las promociones disponibles.
        """

        # Construimos el mensaje de promociones
        message = self.catalog_service.build_promotions_message()

        # Enviamos el mensaje al cliente
        return await self.whatsapp_client.send_text(phone, message)

    async def send_gift_options(self, phone: str) -> dict:
        """
        Envía opciones de productos para regalo.
        """

        message = (
            "Tenemos varias opciones para regalo 🎁\n\n"
            "📒 Agenda personalizada\n"
            "🔑 Llavero personalizado\n"
            "📱 Portacelular en madera\n"
            "🖼️ Portarretrato LED\n"
            "🎨 Cuadros personalizados\n\n"
            "Cuéntanos para quién es el regalo y qué estilo quieres."
        )

        return await self.whatsapp_client.send_text(phone, message)

    async def send_human_support(self, phone: str) -> dict:
        """
        Envía un mensaje indicando que será atendido por una persona.
        """

        message = (
            "Perfecto 😊 Te atenderá una persona de Lordart.\n\n"
            "Por favor envíanos:\n"
            "- Producto que te interesa\n"
            "- Nombre o frase a personalizar\n"
            "- Fecha para la que lo necesitas"
        )

        return await self.whatsapp_client.send_text(phone, message)

    async def send_channel_link(self, phone: str) -> dict:
        """
        Envía el enlace del canal de WhatsApp de Lordart.
        """

        message = (
            "Claro 😊 Puedes seguir nuestro canal de Lordart para ver novedades, "
            "productos nuevos y promociones:\n\n"
            "https://whatsapp.com/channel/0029Vb87orn9cDDhSi2MKV2W"
        )

        return await self.whatsapp_client.send_text(phone, message)

    async def send_product_detail(self, phone: str, product_id: int) -> dict:
        """
        Envía el detalle de un producto específico.

        Si el producto tiene imagen real, la envía.
        Si no tiene imagen real, envía solo texto.
        """

        # Buscamos el producto por ID
        product = self.catalog_service.get_product_by_id(product_id)

        # Si no existe el producto, mostramos mensaje de ayuda
        if not product:
            return await self.send_default(phone)

        # Armamos la descripción del producto
        caption = (
            f"{product['nombre']}\n\n"
            f"{product['descripcion']}\n"
            f"Precio: ${product['precio']:,}\n\n"
            "¿Quieres personalizar este producto?"
        )

        # Obtenemos la URL de imagen
        image_url = product.get("imagen")

        # Si la imagen es real y no es example.com, enviamos imagen
        if image_url and "example.com" not in image_url:
            return await self.whatsapp_client.send_image_by_url(phone, image_url, caption)

        # Si no hay imagen real, enviamos solo texto
        return await self.whatsapp_client.send_text(phone, caption)

    async def send_channel_post_to_admin(self, phone: str) -> dict:
        """
        Genera un texto para publicar en el canal y se lo envía al administrador.

        Si ADMIN_PHONE está configurado en .env, se envía a ese número.
        Si no está configurado, se envía al mismo número que pidió el comando.
        """

        # Generamos el texto de publicación
        post = self.channel_post_service.generate_promotion_post()

        # Definimos a quién se le enviará el borrador
        admin_phone = settings.admin_phone or phone

        # Mensaje final para el administrador
        message = (
            "Texto sugerido para publicar manualmente en el canal de Lordart:\n\n"
            f"{post}"
        )

        return await self.whatsapp_client.send_text(admin_phone, message)

    async def send_default(self, phone: str) -> dict:
        """
        Mensaje por defecto cuando el bot no entiende lo que escribió el cliente.
        """

        message = (
            "No entendí muy bien tu mensaje 😅\n\n"
            "Puedes escribir:\n"
            "- hola\n"
            "- catálogo\n"
            "- promociones\n"
            "- regalo\n"
            "- asesor\n"
            "- canal"
        )

        return await self.whatsapp_client.send_text(phone, message)