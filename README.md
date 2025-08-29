# Detection de Bad Buzz

[![Statut de la Build](https://img.shields.io/github/actions/workflow/status/votre_utilisateur/detection-de-bad-buzz/main.yml?style=flat-square)](https://github.com/votre_utilisateur/detection-de-bad-buzz/actions)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Ce projet a pour but de détecter le "bad buzz" en analysant le sentiment (positif ou négatif) de commentaires textuels. Il est composé d'une API de machine learning construite avec FastAPI et d'une interface utilisateur interactive développée avec Streamlit.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Déploiement](#déploiement)
- [Lancer les tests](#lancer-les-tests)
- [Construit avec](#construit-avec)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Contact](#contact)

## Fonctionnalités

- 🚀 **API de prédiction** : Un endpoint FastAPI pour analyser un texte et retourner son sentiment (positif/négatif) ainsi qu'un score de confiance.
- 🎨 **Interface utilisateur intuitive** : Une application Streamlit permettant de tester le modèle en direct en saisissant du texte.
- 🐳 **Containerisation** : Le projet est entièrement "dockerisé", assurant une portabilité et une mise en production simplifiées.

## Architecture

Le projet est divisé en deux services principaux :

1. **Backend (API FastAPI)** :

   - Sert le modèle de deep learning (Keras/TensorFlow).
   - Expose un endpoint `/predict/` pour les requêtes d'analyse.
   - Gère le prétraitement du texte.
2. **Frontend (App Streamlit)** :

   - Fournit une interface web pour les utilisateurs.
   - Communique avec l'API FastAPI pour obtenir les prédictions.
   - Affiche les résultats de manière claire et visuelle.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants sur votre machine.

- Python (3.9 ou supérieure)
- pip (généralement inclus avec Python)
- Docker
- Google Cloud SDK (Optionnel, pour le déploiement sur GCP)

## Installation

Suivez ces étapes pour mettre en place votre environnement de développement.

1. **Clonez le dépôt**

   ```sh
   git clone https://github.com/votre_utilisateur/detection-de-bad-buzz.git
   cd detection-de-bad-buzz
   ```
2. **Installez les dépendances**

   Il est recommandé d'utiliser un environnement virtuel.

   ```sh
   python -m venv badbuzzenv
   source badbuzzenv/bin/activate  # Sur Windows: badbuzzenv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configurez les variables d'environnement**

   Pour que l'API puisse télécharger les fichiers du modèle, vous devez héberger `config.json`, `model.weights.h5` et `tokenizer_bidirectional_gru_en.pickle` et fournir leurs URLs.

   Créez un fichier `.env` à la racine du projet et ajoutez-y les lignes suivantes :

   ```
   MODEL_CONFIG_URL="URL_VERS_VOTRE_config.json"
   MODEL_WEIGHTS_URL="URL_VERS_VOTRE_model.weights.h5"
   TOKENIZER_URL="URL_VERS_VOTRE_tokenizer.pickle"
   ```

## Utilisation

Pour lancer l'application en local, vous devez démarrer les deux services dans des terminaux séparés.

1. **Lancez l'API FastAPI**

   ```sh
   uvicorn api:app --reload
   ```

   L'API sera accessible à l'adresse `http://127.0.0.1:8000`.
2. **Lancez l'application Streamlit**

   ```sh
   streamlit run sentiment_app.py
   ```

   L'interface utilisateur sera accessible à l'adresse `http://localhost:8501`.

## Déploiement

Le déploiement se fait via la containerisation avec Docker, puis l'hébergement sur Google Cloud Platform (GCP).

### 1. Construire l'image Docker

Assurez-vous que votre `Dockerfile` est configuré pour exposer le port de l'API (par exemple, 8000).

```sh
docker build -t detection-bad-buzz-api .
```
