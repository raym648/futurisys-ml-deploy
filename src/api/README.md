---
title: Futurisys API
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 7860
tags:
  - machine-learning
  - fastapi
  - docker
  - ml-deployment
pinned: false
short_description: API FastAPI pour déployer un modèle de Machine Learning
---

# 🚀 Futurisys API – ML Deployment

**Futurisys API** est une API **FastAPI** permettant d’exposer un modèle de **Machine Learning** entraîné et sérialisé (`.joblib`).  
Ce projet s’inscrit dans le cadre du **Projet 5 – Déployez un modèle de Machine Learning**.

L’API est conçue pour être :
- ✅ exécutée dans un **conteneur Docker**
- ✅ déployée sur **Hugging Face Spaces (Docker SDK)**
- ✅ consommée par des applications externes (front, Streamlit, etc.)

---

## 🧠 Fonctionnalités

- Chargement d’un modèle ML (`joblib`)
- Endpoint(s) de prédiction
- API REST exposée via **FastAPI**
- Documentation automatique
- Déploiement simple via Docker

---

## 🐳 Déploiement (Docker / Hugging Face Space)

Cette application utilise le **SDK Docker** de Hugging Face.

### 🔹 Port exposé
L’API écoute sur le port :

```text
7860
```

---

## Démarrage local

1. ***Créer et activer un environnement Python (3.10+)***
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. ***Placer le modèle sous models/model.joblib (ou adapter MODEL_PATH dans app/main.py).***

3. ***Lancer l'API:***
```bash
uvicorn app.main:app --reload --port 8000
```

4. ***Docs automatiques:***
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
