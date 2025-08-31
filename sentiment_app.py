import streamlit as st
import requests
import os
import time

# --- CONFIGURATION DE LA PAGE ET STYLE CSS ---

# NOTE : Ce paramètre doit être identique à celui utilisé lors de l'entraînement du modèle.
# Le fichier config.json indique une longueur de 50.
MAX_SEQUENCE_LENGTH = 50

st.set_page_config(
    page_title="Analyse de Sentiment",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="auto"
)

# Injection de CSS personnalisé pour un design sophistiqué
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
}

/* Thème sombre général */
.stApp {
    background-color: #121212;
    color: #E0E0E0;
}

/* Titre principal */
h1 {
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
    color: #03DAC6; /* Sarcelle vibrant, courant dans les UI modernes */
    text-align: center;
    padding-bottom: 20px;
}

/* Zone de texte pour le commentaire */
.stTextArea textarea {
    background-color: #1E1E1E;
    color: #E0E0E0;
    border: 1px solid #333333;
    border-radius: 8px;
    font-size: 1rem;
    height: 150px;
    padding: 12px;
    transition: border-color 0.3s;
}

.stTextArea textarea:focus {
    border-color: #03DAC6; /* Mise en évidence lors de la sélection */
}

/* Bouton d'analyse */
.stButton>button {
    border: 2px solid #03DAC6;
    border-radius: 25px;
    color: #03DAC6;
    background-color: transparent;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease-in-out;
    display: block;
    margin: 20px auto 0 auto; /* Centrer le bouton */
}

.stButton>button:hover {
    background-color: #03DAC6;
    color: #121212; /* Texte sombre au survol */
    box-shadow: 0 0 15px #03DAC6;
}

/* Conteneurs personnalisés pour les résultats */
.result-container {
    padding: 25px;
    border-radius: 10px;
    margin-top: 25px;
    text-align: center;
    border-left: 5px solid;
}

.positive {
    border-color: #00BFA6; /* Vert pour le positif */
    background-color: rgba(0, 191, 166, 0.1);
}

.negative {
    border-color: #FF5252; /* Rouge pour le négatif */
    background-color: rgba(255, 82, 82, 0.1);
}

.result-header {
    font-size: 2rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px; /* Espace entre l'icône et le texte */
}

.positive-text {
    color: #00BFA6;
}

.negative-text {
    color: #FF5252;
}

.score-text {
    font-size: 1.1rem;
    color: #A0A0A0;
    margin-top: 10px;
}
</style>""", unsafe_allow_html=True)


# --- INTERFACE PRINCIPALE DE L'APPLICATION ---

st.title("🎭 Analyseur de Sentiment")

# Le nom du fichier tokenizer suggère que le modèle est entraîné sur de l'anglais.
st.markdown(
    "Entrez un commentaire (en **anglais**) ci-dessous et notre IA prédira si le sentiment est **positif** ou **négatif**."
)

# --- API Configuration ---
# Lit l'URL de l'API depuis une variable d'environnement, avec une valeur par défaut pour le local
#API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict/")
#API_URL="https://deploiement-783259175753.europe-west1.run.app/predict/"
API_URL="https://badbuzzdetector-783259175753.europe-west9.run.app/predict/"
# Utilisation d'un formulaire pour regrouper le champ de texte et le bouton
with st.form(key='sentiment_form'):
    user_input = st.text_area(
        label="Votre commentaire :",
        placeholder="Ex: 'This movie was absolutely fantastic, the acting was superb!'",
        height=150
    )
    submit_button = st.form_submit_button(label='Analyser le Sentiment')

# --- LOGIQUE DE PRÉDICTION ET AFFICHAGE ---
if submit_button and user_input:
    with st.spinner('Analyse en cours...'):
        try:
            # --- Appel à l'API FastAPI ---
            payload = {"text": user_input}
            response = requests.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

            result = response.json()
            score = result["score"]
            sentiment_text = result["sentiment"]

            # --- Affichage du résultat ---
            sentiment_class = "positive" if sentiment_text == "Positif" else "negative"
            icon = "👍" if sentiment_text == "Positif" else "👎"

            st.markdown(f"""
                <div class="result-container {sentiment_class}">
                    <div class="result-header {sentiment_class}-text">
                        {icon} {sentiment_text}
                    </div>
                    <p class="score-text">Score de confiance : <strong>{score:.2%}</strong></p>
                </div>
            """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            st.info("Assurez-vous que le serveur FastAPI est bien lancé sur http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {e}")

elif submit_button and not user_input:
    st.warning("Veuillez entrer un commentaire à analyser.")
