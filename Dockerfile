# --- Étape 1: Le "Builder" ---
# Cette étape installe les dépendances dans un environnement isolé.
FROM python:3.9-slim as builder

# Définir les variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installer les dépendances
COPY requirements-api.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-api.txt


# --- Étape 2: L'image finale ---
# Cette étape construit l'image de production finale, plus légère et sécurisée.
FROM python:3.9-slim

# Définir les mêmes variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Créer un utilisateur non-root pour des raisons de sécurité
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Définir le répertoire de travail pour l'utilisateur non-root
WORKDIR /home/appuser

# Copier les dépendances installées depuis l'étape "builder"
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code de l'application et donner les permissions à notre utilisateur
COPY api.py .
RUN chown -R appuser:appgroup /home/appuser

# Changer d'utilisateur pour ne plus être root
USER appuser

# Exposer le port et lancer l'application
EXPOSE 8080
CMD exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT api:app