# json permite leer archivos .json
import json

# Path permite manejar rutas de archivos de forma segura
from pathlib import Path


class CatalogService:
    """
    Servicio encargado de manejar catálogo y promociones.

    Por ahora usa archivos JSON:
    - products.json
    - promotions.json

    Más adelante puedes cambiar esto por una base de datos.
    """

    def __init__(self):
        """
        Constructor del servicio.

        Aquí definimos dónde están ubicados los archivos JSON.
        """

        # Ruta base hacia la carpeta app/data
        self.base_path = Path(__file__).resolve().parent.parent / "data"

        # Archivo donde están los productos
        self.products_file = self.base_path / "products.json"

        # Archivo donde están las promociones
        self.promotions_file = self.base_path / "promotions.json"

    def get_products(self) -> list[dict]:
        """
        Lee y retorna todos los productos del archivo products.json.
        """

        with open(self.products_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_promotions(self) -> list[dict]:
        """
        Lee y retorna todas las promociones del archivo promotions.json.
        """

        with open(self.promotions_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def build_catalog_message(self) -> str:
        """
        Construye un mensaje de texto con el catálogo completo.

        Este texto es el que luego se envía por WhatsApp.
        """

        # Obtenemos los productos desde el JSON
        products = self.get_products()

        # Encabezado del mensaje
        message = "Catálogo Lordart 🎨\n\n"

        # Recorremos cada producto para agregarlo al mensaje
        for product in products:
            message += (
                f"{product['id']}. {product['nombre']}\n"
                f"   Precio: ${product['precio']:,}\n"
                f"   {product['descripcion']}\n\n"
            )

        # Cierre del mensaje
        message += "Responde con el número del producto que quieres ver."

        return message

    def build_promotions_message(self) -> str:
        """
        Construye un mensaje de texto con las promociones disponibles.
        """

        # Obtenemos las promociones desde el JSON
        promotions = self.get_promotions()

        # Encabezado del mensaje
        message = "Promociones disponibles 🎁\n\n"

        # Agregamos cada promoción al mensaje
        for promo in promotions:
            message += (
                f"{promo['id']}. {promo['titulo']}\n"
                f"   Precio: ${promo['precio']:,}\n"
                f"   {promo['descripcion']}\n\n"
            )

        # Cierre del mensaje
        message += "¿Quieres que te enviemos fotos o más información?"

        return message

    def get_product_by_id(self, product_id: int) -> dict | None:
        """
        Busca un producto por su ID.

        Si lo encuentra, retorna el producto.
        Si no lo encuentra, retorna None.
        """

        # Cargamos todos los productos
        products = self.get_products()

        # Buscamos el producto que coincida con el ID
        for product in products:
            if product["id"] == product_id:
                return product

        # Si no se encuentra el producto
        return None