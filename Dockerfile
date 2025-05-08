# Usar una imagen base de Python ligera
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del proyecto al contenedor
COPY . /app

# Copiar explícitamente el archivo de configuración (opcional, ya está incluido con el COPY anterior)
COPY config.conf /app/config.conf

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exponer el puerto que Gunicorn usará
EXPOSE 8080

# Comando para iniciar la app usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
