# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Git installieren
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Kopiere das Flask-Projekt
COPY . .

# Umgebungsvariablen setzen
ENV FLASK_APP=wsgi.py

# Skript zum Überprüfen von Updates
COPY check_updates.sh /usr/local/bin/check_updates.sh
RUN chmod +x /usr/local/bin/check_updates.sh

# Starte den Flask-Server im Hintergrund
CMD ["sh", "-c", "while true; do /usr/local/bin/check_updates.sh; sleep 900; done & flask run --host=0.0.0.0 --port=5000"]
