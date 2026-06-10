# Importamos BaseSettings para leer variables de entorno desde .env
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Esta clase centraliza toda la configuración del proyecto.

    Aquí leemos los datos sensibles desde el archivo .env:
    - Token de WhatsApp
    - Phone Number ID
    - WhatsApp Business Account ID
    - Verify Token
    - Versión de Graph API
    """

    # Token que Meta genera para poder usar la API de WhatsApp
    whatsapp_token: str

    # ID del número de teléfono que usará el bot para enviar mensajes
    phone_number_id: str

    # ID de la cuenta de WhatsApp Business
    whatsapp_business_account_id: str

    # Token inventado por nosotros para verificar el webhook
    verify_token: str

    # Versión de la API de Meta
    graph_api_version: str = "v25.0"

    # Número del administrador del bot
    admin_phone: str | None = None

    # Puerto donde correrá la app
    app_port: int = 3000

    class Config:
        """
        Configuración interna de Pydantic.

        env_file = ".env"
        indica que las variables se leerán desde un archivo .env.
        """

        env_file = ".env"
        extra = "ignore"


# Creamos una instancia global de configuración.
# Esta variable se importa en otros archivos.
settings = Settings()