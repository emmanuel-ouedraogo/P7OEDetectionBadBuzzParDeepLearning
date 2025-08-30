# Detection de Bad Buzz

[![Statut de la Build](https://img.shields.io/github/actions/workflow/status/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/main.yml?style=flat-square)](https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/actions)
[![Licence](https://img.shields.io/github/license/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning?style=flat-square)](https://opensource.org/licenses/MIT)

Ce projet a pour but de détecter le "bad buzz" en analysant le sentiment (positif ou négatif) de commentaires textuels. Il est composé d'une API de machine learning construite avec FastAPI et d'une interface utilisateur interactive développée avec Streamlit.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [🏗️ Structure du Projet](#️-structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Déploiement](#déploiement)
- [Lancer les tests](#lancer-les-tests)
- [Construit avec](#construit-avec)
- [🤝 Contribuer](#-contribuer)
- [Licence](#licence)
- [Contact](#contact)

## Fonctionnalités

- 🚀 **API de prédiction** : Un endpoint FastAPI pour analyser un texte et retourner son sentiment (positif/négatif) ainsi qu'un score de confiance.
- 🎨 **Interface utilisateur intuitive** : Une application Streamlit permettant de tester le modèle en direct en saisissant du texte.
- 🐳 **Containerisation** : L'API est entièrement "dockerisée", assurant une portabilité et une mise en production simplifiées sur n'importe quel service cloud.

## Architecture

Le projet est divisé en deux services principaux :

1. **Backend (API FastAPI)** :

   - Charge le modèle de deep learning (Keras/TensorFlow) au démarrage.
   - Expose un endpoint `/predict/` pour les requêtes d'analyse.
   - Gère le prétraitement du texte et la prédiction.
   - Conçu pour être déployé comme un conteneur Docker.

2. **Frontend (App Streamlit)** :

   - Fournit une interface web pour les utilisateurs.
   - Communique avec l'API FastAPI pour obtenir les prédictions.
   - Affiche les résultats de manière claire et visuelle.
   - Conçu pour être lancé localement ou déployé sur des plateformes comme Streamlit Community Cloud.

## 🏗️ Structure du Projet

Le dépôt est organisé comme suit pour une meilleure clarté :

```
.
├── badbuzzenv/           # Environnement virtuel (ignoré par .gitignore)
├── api.py                # Le code de l'API FastAPI (backend)
├── sentiment_app.py      # Le code de l'application Streamlit (frontend)
├── Dockerfile            # Instructions pour construire l'image Docker de l'API
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Fichier pour les variables d'environnement locales (non versionné)
├── .dockerignore         # Fichiers à exclure du build Docker
└── README.md             # Ce fichier
```

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants sur votre machine.

- Python (3.9 ou supérieure)
- pip (généralement inclus avec Python)
- Docker (pour construire et déployer l'API)
- Google Cloud SDK (Optionnel, pour le déploiement sur GCP)

## Installation

Suivez ces étapes pour mettre en place votre environnement de développement.

1. **Clonez le dépôt**

   ```sh
   git clone https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning.git
   cd P7OEDetectionBadBuzzParDeepLearning
   ```
2. **Installez les dépendances**
   
   L'utilisation d'un environnement virtuel est une bonne pratique pour isoler les dépendances du projet.

   ```sh
   # Créer l'environnement virtuel
   python -m venv badbuzzenv
   
   # Activer l'environnement
   source badbuzzenv/bin/activate  # Sur Windows: badbuzzenv\Scripts\activate
   
   # Installer les paquets requis
   pip install -r requirements.txt
   ```
3. **Configurez les variables d'environnement**

   Créez un fichier `.env` à la racine du projet et ajoutez-y les lignes suivantes :

   ```
   # URLs pour télécharger les artefacts du modèle
   MODEL_CONFIG_URL="https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/config.json"
   MODEL_WEIGHTS_URL="https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/model.weights.h5"
   TOKENIZER_URL="https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/tokenizer_bidirectional_gru_en.pickle"
   ```

## Utilisation

Pour lancer l'application en local, vous devez démarrer les deux services (API et interface utilisateur) dans **deux terminaux séparés**. Assurez-vous que votre environnement virtuel est activé dans les deux.

1. **Lancez l'API FastAPI**

   Dans votre premier terminal :
   ```sh
   uvicorn api:app --reload
   ```
   - L'API sera accessible à l'adresse `http://127.0.0.1:8000`.
   - La documentation interactive de l'API (générée automatiquement par FastAPI) sera disponible sur `http://127.0.0.1:8000/docs`.

2. **Lancez l'application Streamlit**

   Dans votre second terminal :
   ```sh
   streamlit run sentiment_app.py
   ```
   - L'interface utilisateur s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

## Déploiement

Le déploiement de cette architecture se fait en deux temps : d'abord l'API, puis l'interface Streamlit.

### 1. Déployer l'API sur Google Cloud Run (GCP)

Cloud Run est une plateforme serverless idéale pour déployer des conteneurs. Elle gère automatiquement la mise à l'échelle, y compris la mise à l'échelle à zéro (vous ne payez que lorsque votre API est utilisée).

#### Prérequis pour GCP

- Avoir un compte Google Cloud avec un projet créé et la facturation activée.
- Avoir installé et initialisé le Google Cloud SDK.

#### Étapes de déploiement

1.  **Authentification et configuration du projet**
    
    Connectez-vous à votre compte et définissez votre projet par défaut.
    ```sh
    # Ouvre une fenêtre de navigateur pour la connexion
    gcloud auth login
    
    # Remplacez [VOTRE_PROJECT_ID] par l'ID de votre projet GCP
    gcloud config set project [VOTRE_PROJECT_ID]
    ```

2.  **Activez les APIs nécessaires** (à faire une seule fois par projet)
    ```sh
    gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
    ```

3.  **Déployez l'application API**
    
    Lancez la commande suivante depuis la racine de votre projet. Elle s'occupe de tout : construire l'image Docker, la stocker et la déployer.

    > **Note :** Remplacez `europe-west1` par la région GCP de votre choix (ex: `us-central1`).

    ```sh
    gcloud run deploy detection-bad-buzz-api \ # Nom de votre service sur Cloud Run
      --source . \                             # Déployer depuis le code source local
      --platform=managed \                     # Utiliser la plateforme entièrement gérée
      --region=europe-west1 \                  # Région de déploiement
      --allow-unauthenticated \                # Autoriser les appels publics (nécessaire pour Streamlit)
      --set-env-vars="MODEL_CONFIG_URL=https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/config.json,MODEL_WEIGHTS_URL=https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/model.weights.h5,TOKENIZER_URL=https://github.com/emmanuel-ouedraogo/P7OEDetectionBadBuzzParDeepLearning/releases/download/V1.O.O/tokenizer_bidirectional_gru_en.pickle"
    ```
    Une fois la commande terminée, `gcloud` affichera l'URL de votre API déployée. Conservez-la pour l'étape suivante.

### 2. Déployer l'interface Streamlit

L'interface Streamlit peut être déployée sur de nombreuses plateformes. Streamlit Community Cloud est une option gratuite et très simple.

1.  Poussez votre code sur un dépôt GitHub (c'est déjà fait !).
2.  Connectez-vous à share.streamlit.io avec votre compte GitHub.
3.  Cliquez sur "New app" et sélectionnez votre dépôt.
4.  Dans les "Advanced settings...", allez dans la section "Secrets".
5.  Ajoutez un secret pour indiquer à l'application Streamlit où trouver l'API. Le contenu du secret doit être :
    ```toml
    # Remplacez par l'URL de votre API déployée sur Cloud Run
    API_URL = "https://detection-bad-buzz-api-xxxxxxxxxx-ew.a.run.app/predict/"
    ```
6.  Cliquez sur "Deploy!".

## Lancer les tests

Pour exécuter les tests (à venir), installez `pytest` et lancez-le depuis la racine du projet.

```sh
pip install pytest
pytest
```

## Construit avec

- **Backend** : FastAPI, Gunicorn, TensorFlow/Keras
- **Frontend** : Streamlit
- **Déploiement** : Docker, Google Cloud Run

## 🤝 Contribuer

Les contributions sont ce qui fait de la communauté open source un endroit incroyable pour apprendre, inspirer et créer. Toute contribution que vous faites est **grandement appréciée**.

Veuillez lire `CONTRIBUTING.md` pour plus de détails sur le processus.

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## Contact

Emmanuel OUEDRAOGO - Lien du projet

---
