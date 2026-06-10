# Imagen base liviana de Python
FROM python:3.11-slim

# Carpeta interna donde vivirá el proyecto dentro del contenedor
WORKDIR /app

# Copiamos primero requirements para aprovechar caché de Docker
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto al contenedor
COPY . .

# Exponemos el puerto donde correrá FastAPI
EXPOSE 3000

# Comando para iniciar FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]