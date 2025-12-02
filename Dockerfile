# Usar Python 3.11 slim
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos necesarios
COPY predictor_lsm.py .
COPY servidor.py .
COPY mejor_modelo.pkl .
COPY scaler.pkl .
COPY label_encoder.pkl .
COPY templates/ ./templates/

# Exponer puerto 3000
EXPOSE 3000

# Variable de entorno para Flask
ENV FLASK_APP=servidor.py
ENV PYTHONUNBUFFERED=1

# Comando para iniciar el servidor
CMD ["python", "servidor.py"]
