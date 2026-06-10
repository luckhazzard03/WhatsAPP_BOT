# Importamos el servicio de catálogo para reutilizar promociones
from app.services.catalog_service import CatalogService


class ChannelPostService:
    """
    Servicio para generar textos de publicación para el canal de Lordart.

    Importante:
    Este servicio NO publica automáticamente en el canal de WhatsApp.

    Lo que hace es generar un texto listo para copiar y pegar manualmente.
    """

    def __init__(self):
        """
        Constructor del servicio.

        Usamos CatalogService para leer las promociones actuales.
        """

        self.catalog_service = CatalogService()

    def generate_promotion_post(self) -> str:
        """
        Genera un texto promocional para el canal de WhatsApp.

        Este texto se puede enviar al administrador para que lo publique manualmente.
        """

        # Obtenemos las promociones disponibles
        promotions = self.catalog_service.get_promotions()

        # Encabezado de la publicación
        message = "Novedades Lordart 🎨✨\n\n"
        message += "Tenemos detalles personalizados para regalar y sorprender.\n\n"

        # Agregamos cada promoción al texto
        for promo in promotions:
            message += (
                f"🎁 {promo['titulo']}\n"
                f"{promo['descripcion']}\n"
                f"Precio: ${promo['precio']:,}\n\n"
            )

        # Agregamos el enlace del canal de Lordart
        message += (
            "Escríbenos para personalizar tu detalle.\n"
            "Canal Lordart: https://whatsapp.com/channel/0029Vb87orn9cDDhSi2MKV2W"
        )

        return message