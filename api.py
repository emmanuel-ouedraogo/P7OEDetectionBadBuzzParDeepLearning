import pickle
import numpy as np
import tensorflow as tf
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import uvicorn

# --- Helper pour le déploiement ---
def download_file_if_not_exists(url, local_path):
    """Télécharge un fichier depuis une URL s'il n'existe pas localement."""
    if not os.path.exists(local_path):
        print(f"Téléchargement de {local_path} depuis {url}...")
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Téléchargement de {local_path} terminé.")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du téléchargement de {url}: {e}")
            # Si le téléchargement échoue, le programme s'arrêtera plus tard
            # car le fichier sera manquant.
            raise


# --- Configuration ---
MAX_SEQUENCE_LENGTH = 50
MODEL_CONFIG_PATH = "config.json"
MODEL_WEIGHTS_PATH = "model.weights.h5"
TOKENIZER_PATH = "tokenizer_bidirectional_gru_en.pickle"

# --- Modèle de données Pydantic pour la validation des requêtes ---
class Comment(BaseModel):
    text: str

# --- Chargement du modèle et du tokenizer ---
def load_model_and_tokenizer():
    """
    Charge le modèle Keras et le tokenizer une seule fois au démarrage.
    """
    try:
        # Récupérer les URLs depuis les variables d'environnement
        config_url = os.getenv("MODEL_CONFIG_URL")
        weights_url = os.getenv("MODEL_WEIGHTS_URL")
        tokenizer_url = os.getenv("TOKENIZER_URL")

        # Télécharger les fichiers s'ils ne sont pas présents
        download_file_if_not_exists(config_url, MODEL_CONFIG_PATH)
        download_file_if_not_exists(weights_url, MODEL_WEIGHTS_PATH)
        download_file_if_not_exists(tokenizer_url, TOKENIZER_PATH)

        # Charger la configuration du modèle depuis le fichier JSON
        with open(MODEL_CONFIG_PATH, 'r') as json_file:
            loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
        # Charger les poids dans l'architecture du modèle
        model.load_weights(MODEL_WEIGHTS_PATH)
        
        # Charger le tokenizer
        with open(TOKENIZER_PATH, 'rb') as handle:
            tokenizer = pickle.load(handle)
            
        return model, tokenizer
    except Exception as e:
        print(f"Erreur lors du chargement des modèles : {e}")
        raise RuntimeError(f"Impossible de charger les modèles : {e}")

# --- Initialisation de l'API FastAPI ---
app = FastAPI(
    title="API d'Analyse de Sentiment",
    description="Une API pour prédire si un commentaire est positif ou négatif.",
    version="1.0.0"
)

# Charger les modèles au démarrage de l'application
model, tokenizer = load_model_and_tokenizer()

# --- Endpoints de l'API ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API d'analyse de sentiment. Utilisez le endpoint /predict/."}

@app.post("/predict/")
def predict_sentiment(comment: Comment):
    if not comment.text.strip():
        raise HTTPException(status_code=400, detail="Le texte du commentaire ne peut pas être vide.")

    # Prétraitement du texte
    sequence = tokenizer.texts_to_sequences([comment.text])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    
    # Prédiction
    prediction = model.predict(padded_sequence)
    score = float(prediction[0][0]) # Assurer la compatibilité JSON
    
    # Déterminer le sentiment
    sentiment = "Positif" if score > 0.5 else "Négatif"
    
    return {"text": comment.text, "sentiment": sentiment, "score": score}