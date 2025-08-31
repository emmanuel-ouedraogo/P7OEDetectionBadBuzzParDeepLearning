from dotenv import load_dotenv
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

import pickle
import numpy as np
# --- Optimisation de la mémoire pour TensorFlow ---
# Limiter le nombre de threads que TensorFlow peut utiliser pour réduire la consommation de RAM.
# Ces variables d'environnement sont une autre façon de définir ces valeurs.
# Nous les mettons ici pour plus de clarté et de contrôle.
import os
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
import tensorflow as tf
import requests
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import uvicorn


# --- Helper pour le déploiement ---
def download_file_if_not_exists(url, local_path):
    """Télécharge un fichier depuis une URL s'il n'existe pas localement."""
    if not os.path.exists(local_path):
        # Créer le répertoire parent si nécessaire
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
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
        # Récupérer les URLs depuis les variables d'environnement et valider leur présence
        env_vars = {
            "MODEL_CONFIG_URL": os.getenv("MODEL_CONFIG_URL"),
            "MODEL_WEIGHTS_URL": os.getenv("MODEL_WEIGHTS_URL"),
            "TOKENIZER_URL": os.getenv("TOKENIZER_URL"),
        }

        missing_vars = [key for key, value in env_vars.items() if not value]
        if missing_vars:
            raise EnvironmentError(
                f"Les variables d'environnement suivantes sont manquantes : {', '.join(missing_vars)}. "
                "Veuillez vous référer au README.md pour les configurer."
            )

        # Télécharger les fichiers s'ils ne sont pas présents
        download_file_if_not_exists(env_vars["MODEL_CONFIG_URL"], MODEL_CONFIG_PATH)
        download_file_if_not_exists(env_vars["MODEL_WEIGHTS_URL"], MODEL_WEIGHTS_PATH)
        download_file_if_not_exists(env_vars["TOKENIZER_URL"], TOKENIZER_PATH)

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
        raise RuntimeError("Impossible de charger les modèles.") from e

# --- Initialisation de l'API FastAPI ---
app = FastAPI(
    title="API d'Analyse de Sentiment",
    description="Une API pour prédire si un commentaire est positif ou négatif.",
    version="1.0.0"
)

# Déclarer les variables du modèle comme globales pour qu'elles soient accessibles
# par les endpoints après avoir été chargées lors du démarrage.
model = None
tokenizer = None

@app.on_event("startup")
async def startup_event():
    """Charge le modèle au démarrage de l'application FastAPI."""
    global model, tokenizer
    print("Démarrage de l'application, chargement du modèle...")
    model, tokenizer = load_model_and_tokenizer()
    print("Modèle chargé avec succès.")

# --- Endpoints de l'API ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API d'analyse de sentiment. Utilisez le endpoint /predict/."}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(response: Response):
    """Vérifie si le modèle est chargé et si l'API est prête à servir des requêtes."""
    if model is not None and tokenizer is not None:
        return {"status": "ok", "message": "Le modèle est chargé et prêt."}
    else:
        # Si le modèle n'est pas prêt, renvoyer un statut 503 Service Unavailable
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable", "message": "Le modèle est en cours de chargement. Veuillez patienter."}

@app.post("/predict/")
def predict_sentiment(comment: Comment):
    if not comment.text.strip():
        raise HTTPException(status_code=400, detail="Le texte du commentaire ne peut pas être vide.")
    
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Le modèle n'est pas encore prêt. Veuillez réessayer dans un instant.")

    # Prétraitement du texte
    sequence = tokenizer.texts_to_sequences([comment.text])
    padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    
    # Prédiction
    prediction = model.predict(padded_sequence)
    score = float(prediction[0][0]) # Assurer la compatibilité JSON
    
    # Déterminer le sentiment
    sentiment = "Positif" if score > 0.5 else "Négatif"
    
    return {"text": comment.text, "sentiment": sentiment, "score": score}