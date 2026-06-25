# Usa una imagen base ligera de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los requerimientos y los instala
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copia el resto del código fuente del juego
COPY . .

# Exponer el puerto que usará Flask
EXPOSE 5000

# Variables de entorno para que Flask escuche en todas las interfaces y deshabilite el buffering
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend/src

# Comando por defecto para correr la aplicación
CMD ["python", "app.py"]
