# Futurisys – Déploiement d’un Modèle de Machine Learning

## 📌 Présentation du projet

Ce projet s’inscrit dans le **Projet‑5 – Déployez un modèle de Machine Learning**. Il vise à exposer un modèle de classification via une API FastAPI, à assurer la traçabilité complète des données et des prédictions dans PostgreSQL (Neon serverless), et à fournir un dashboard de visualisation déployé sur Hugging Face Spaces.

Le projet adopte une approche **MLOps** : versionnement des artefacts, tests automatisés, CI/CD, monitoring et documentation.

---

## 🧠 Modèle de Machine Learning

* **Type** : Classification binaire
* **Modèle par défaut** : `random_forest_e04`
* **Pipeline** : SMOTE + RandomForest
* **Artefacts** : `.joblib`, `.npy`, `.csv`
* **Frameworks** : scikit‑learn, numpy

Le modèle est chargé dynamiquement sans ré‑entraînement lors du déploiement.

---

## 🚀 API FastAPI

L’API expose plusieurs endpoints :

* `/predict` – prédiction à partir d’un payload JSON
* `/metadata` – informations sur le projet et le modèle
* `/models` – modèles disponibles et modèle par défaut
* `/metrics` – métriques de performance

La documentation interactive est disponible via **Swagger/OpenAPI**.

---

## 🗄️ Base de données

* **SGBD** : PostgreSQL
* **Hébergement** : Neon (serverless)
* **ORM** : SQLAlchemy

Toutes les interactions avec le modèle passent par la base :

* données d’entrée (inputs)
* résultats de prédiction (outputs)

Cela garantit la **traçabilité complète** des échanges.

---

## 🧪 Tests & Qualité

* Tests unitaires et fonctionnels avec **Pytest**
* Couverture de code via **pytest‑cov**
* Exécution automatique dans **GitHub Actions**

---

## 🔄 CI/CD

* Lint + tests sur chaque PR (`main`, `dev`)
* Déploiement automatique sur Hugging Face Spaces après validation

---

## 📊 Dashboard

Un dashboard Streamlit permet :

* la consultation des métriques
* la comparaison des modèles
* l’historique des prédictions

---

## 📚 Documentation

La documentation détaillée est disponible dans le dossier `docs/`.

---

## 🛠️ Installation (local)

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://..."
uvicorn src.api.main:app --reload
```

---

## 📌 Auteur & Contexte

Projet réalisé dans le cadre de la formation **Engineer Intelligence Artificielle**.


------------------------------------------------------------------------------------
------------------------------------------------------------------------------------


# Futurisys ML Deploy (futurisys-ml-deploy)

## Contexte
Ce dépôt contient le Proof of Concept (POC) pour déployer le modèle du **Projet 4** en tant que service API (FastAPI) et pour le publier sur un Hugging Face Space (ou autre target).

## Structure du dépôt
- `app/` : code de l'application (API, inference, utilitaires)  
- `app/ml/` : code d'inférence / wrappers modèle  
- `data/` : jeux de données (ne pas committer les données sensibles et les gros raw files)  
- `tests/` : tests unitaires et fonctionnels  
- `docs/` : documentation complémentaire

## Prérequis
- Python 3.10 — 3.12 (recommandé : 3.10 ou 3.12 selon ton environnement)
- Git
- Node.js + npm (pour `commitlint`)
- PostgreSQL
- Compte GitHub (pour CI / Actions) et accès Hugging Face si tu déploies sur HF Spaces

## Conventions & Outils qualité
- Style : PEP8  
- Formatage : `black`  
- Imports : `isort` (profil `black`)  
- Linter : `flake8`  
- Hooks : `pre-commit` (configuration locale par défaut, voir `.pre-commit-config.yaml`)  
- Commit messages : Conventional Commits (validés par `commitlint` au stade `commit-msg`)

## Installation (local — rapide)
```bash
git clone git@github.com:TON_COMPTE/futurisys-ml-deploy.git
cd futurisys-ml-deploy

# Python (venv)
python -m venv .venv
source .venv/bin/activate

# installer runtime + dev tools
pip install -r requirements.txt

# ===========================================================================================
# Installer commitlint dans le projet (recommandé) si le repo n'a pas package.json
npm init -y
npm install --save-dev @commitlint/cli @commitlint/config-conventional
# config minimale
echo "module.exports = { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js

# si tu utilises pip / venv / conda
pip install "black==23.1.0" "isort==5.12.0" "flake8==6.0.0"

# Nettoyer cache pre-commit et réinstaller hooks
rm -rf ~/.cache/pre-commit
pre-commit clean
pre-commit install

# Tester les hooks (fichiers)
pre-commit run --all-files -v

# *******************************************************************************
# Tester le hook commit-msg (2 façons)
# *******************************************************************************
# Méthode A — faire un vrai commit (recommandée)
git commit --allow-empty -m "feat: test commit-msg (should pass)"
# puis pour un message invalide
git commit --allow-empty -m "invalid message"

# Méthode B — test manuel avec un fichier message
echo "invalid message" > .git/COMMIT_EDITMSG
pre-commit run --hook-stage commit-msg -v --commit-msg-filename .git/COMMIT_EDITMSG

# ===========================================================================================
```

## Tests
- Tests unitaires avec `pytest`
- Tests rapides dans CI (pas d'entraînement)
- Pour tests d'intégration lourds, utiliser une pipeline séparée / runners self-hosted

***Commande pour exécuter les tests :***
```
pytest --maxfail=1 --disable-warnings -q
```

***Commande pour générer un rapport de couverture :***
```
pytest --cov=src --cov-report=xml
```

## Reproductibilité
- Fixer seeds dans expérimentations
- Versionner les modèles (nom + date + hash)
- Utiliser artefacts externes (S3 / HF Hub) pour stocker les modèles

## Branching & Commit
- Conventional Commits
- Branches: `feature/`, `bugfix/`, `hotfix/`, `release/`
- PR mandatory, 1 reviewer minimum
