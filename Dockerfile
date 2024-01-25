# Usa una imagen base de Python
FROM python:3.9-slim

# Establece un directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del código al contenedor
COPY . .

# Comando para ejecutar el script
CMD ["python", "./Scrappersql.py"]

