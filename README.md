# Lordart WhatsApp Bot

Bot desarrollado en Python con FastAPI para responder mensajes de WhatsApp usando WhatsApp Business Platform.

El bot permite:

```text
- Recibir mensajes desde WhatsApp
- Responder automáticamente
- Mostrar catálogo
- Mostrar promociones
- Enviar enlace del canal Lordart
- Generar texto sugerido para publicaciones del canal
```

---

## 1. Estructura del proyecto

```text
lordart-whatsapp-bot/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   └── config.py
│   ├── routers/
│   │   └── webhook_router.py
│   ├── services/
│   │   ├── whatsapp_client.py
│   │   ├── bot_service.py
│   │   ├── catalog_service.py
│   │   └── channel_post_service.py
│   └── data/
│       ├── products.json
│       └── promotions.json
│
├── docs/
│   └── META_SETUP.md
│
├── privacy-policy.html
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 2. Variables de entorno

Crear el archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
WHATSAPP_TOKEN=TOKEN_GENERADO_EN_META
PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
VERIFY_TOKEN=
GRAPH_API_VERSION=v25.0
ADMIN_PHONE=573229614
APP_PORT=3000
```

Descripción:

```text
WHATSAPP_TOKEN
Token largo generado en Meta Developers. Sirve para enviar mensajes.

PHONE_NUMBER_ID
ID interno del número de prueba o producción de WhatsApp. No es el número celular.

WHATSAPP_BUSINESS_ACCOUNT_ID
ID de la cuenta de WhatsApp Business.

VERIFY_TOKEN
Texto inventado para validar el webhook con Meta.

GRAPH_API_VERSION
Versión de Graph API usada por Meta.

ADMIN_PHONE
Número del administrador. Va con código de país y sin el signo +.

APP_PORT
Puerto local donde corre FastAPI.
```

---

## 3. Instalación local

Crear entorno virtual con Python 3.11:

```bash
cd ~/PROJECTS/lordart-whatsapp-bot
python3.11 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 4. Levantar el backend

Ejecutar:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

Validar en navegador:

```text
http://localhost:3000
```

Respuesta esperada:

```json
{
  "status": "ok",
  "message": "Lordart WhatsApp Bot funcionando correctamente"
}
```

Documentación de FastAPI:

```text
http://localhost:3000/docs
```

---

## 5. Instalar Cloudflare Tunnel

Validar si está instalado:

```bash
cloudflared version
```

Si no está instalado, descargar paquete `.deb`:

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
cloudflared version
```

---

## 6. Levantar Cloudflare Tunnel

Cloudflare se usa para exponer el backend local con una URL pública HTTPS.

Con FastAPI corriendo en el puerto 3000, abrir otra terminal y ejecutar:

```bash
cloudflared tunnel --url http://localhost:3000
```

Cloudflare entrega una URL parecida a:

```text
https://rebate-immune-planets-representatives.trycloudflare.com
```

El webhook público queda así:

```text
https://rebate-immune-planets-representatives.trycloudflare.com/webhook
```

Esta URL se configura en Meta Developers.

---

## 7. Orden correcto para correr el proyecto

Terminal 1:

```bash
cd ~/PROJECTS/lordart-whatsapp-bot
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 3000
```

Terminal 2:

```bash
cloudflared tunnel --url http://localhost:3000
```

Meta Developers:

```text
Callback URL:
https://URL_CLOUDFLARE/webhook

Verify token:
Lordart
```

---

## 8. Probar webhook local

Probar verificación:

```bash
curl "http://localhost:3000/webhook?hub.mode=subscribe&hub.verify_token=Lordart***_2026&hub.challenge=12345"
```

Respuesta esperada:

```text
12345
```

---

## 9. Probar POST local

```bash
curl -X POST http://localhost:3000/webhook \
-H "Content-Type: application/json" \
-d '{"entry":[{"changes":[{"value":{"messages":[{"from":"573229614078","type":"text","text":{"body":"hola"}}]}}]}]}'
```

Respuesta esperada:

```json
{ "status": "ok" }
```

---

## 10. Probar POST por Cloudflare

```bash
curl -X POST https://URL_CLOUDFLARE/webhook \
-H "Content-Type: application/json" \
-d '{"entry":[{"changes":[{"value":{"messages":[{"from":"573229614078","type":"text","text":{"body":"hola"}}]}}]}]}'
```

Si el token de Meta está correcto, el bot responde al WhatsApp configurado en el campo `from`.

---

## 11. Configuración obligatoria en Meta

En Meta Developers se debe configurar:

```text
Use cases
Connect on WhatsApp
Basic setup
Step 2. Production setup
Configure Webhooks
```

Valores:

```text
Callback URL:
https://URL_CLOUDFLARE/webhook

Verify token:
Lordart***_2026
```

Luego activar:

```text
messages → Subscribed
```

Además, se debe suscribir la app al WABA:

```bash
set -a
source .env
set +a

curl -i -X POST "https://graph.facebook.com/${GRAPH_API_VERSION}/${WHATSAPP_BUSINESS_ACCOUNT_ID}/subscribed_apps" \
-H "Authorization: Bearer ${WHATSAPP_TOKEN}"
```

Respuesta esperada:

```json
{ "success": true }
```

---

## 12. Prueba real desde WhatsApp

Desde el número beneficiario, escribir al número de prueba de Meta:

```text
+1 555 654 8268
```

Mensaje:

```text
hola
```

El backend debe mostrar:

```text
POST /webhook
Texto recibido: hola
```

El bot debe responder con el menú de Lordart.

---

## 13. Comandos útiles

Ver estado de Git:

```bash
git status
```

Agregar cambios:

```bash
git add .
```

Commit recomendado:

```bash
git commit -m "docs: agregar documentacion de configuracion Meta y Cloudflare"
```

Subir cambios:

```bash
git push origin main
```

---

## 14. Seguridad

No subir `.env`.

El `.gitignore` debe incluir:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
*.log
```

Si el token de Meta fue expuesto, generar uno nuevo y actualizar:

```env
WHATSAPP_TOKEN=NUEVO_TOKEN
```

Reiniciar FastAPI después de cambiar `.env`.

---

## 15. Errores comunes

### No responde al escribir desde WhatsApp

Revisar:

```text
- FastAPI corriendo
- Cloudflare corriendo
- URL de Cloudflare vigente
- Webhook verificado
- messages en Subscribed
- App suscrita al WABA con /subscribed_apps
- App en modo Live
```

### Cloudflare cambió la URL

Actualizar Meta con la nueva URL:

```text
https://NUEVA_URL.trycloudflare.com/webhook
```

Luego presionar:

```text
Verify and save
```

### El POST llega vacío

El endpoint debe validar si el body está vacío antes de leer JSON.

### El botón Test de Meta no responde a WhatsApp

El botón Test usa números de prueba falsos. Sirve para comprobar que el webhook recibe POST, no para validar respuesta real al WhatsApp personal.

Para probar respuesta al WhatsApp personal, usar `curl` con el número real o escribir desde el WhatsApp beneficiario.
