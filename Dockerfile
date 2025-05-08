# Usar Python base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exponer el puerto
EXPOSE 8080

# Comando para correr la app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
