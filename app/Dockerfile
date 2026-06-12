FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Esto copia TODO lo que está dentro de tu carpeta app local (incluyendo templates y app.py) hacia el contenedor
COPY . .

EXPOSE 5000

# CORRECCIÓN: Cambiado de main.py a app.py
CMD ["python", "app.py"]