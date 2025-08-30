# Utiliser une image Python officielle comme image de base.
# python:3.9-slim est une bonne option, légère et stable, qui correspond aux prérequis.
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
# Il est copié en premier pour profiter du cache de Docker.
# Les dépendances ne seront réinstallées que si ce fichier change.
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans le conteneur.
COPY ./api.py /app/api.py

# Exposer le port sur lequel l'API va tourner (8000 est le standard pour FastAPI)
EXPOSE 8000

# Commande pour lancer l'application avec Gunicorn et Uvicorn pour la production
# -w 4: lance 4 "worker processes". Un bon point de départ est (2 * CPU cores) + 1.
# -k uvicorn.workers.UvicornWorker: spécifie d'utiliser les workers Uvicorn.
# --bind 0.0.0.0:8000: écoute sur toutes les interfaces réseau sur le port 8000.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "api:app", "--bind", "0.0.0.0:8000"]
