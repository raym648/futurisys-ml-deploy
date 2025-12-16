# API - Futurisys ML Deploy

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

