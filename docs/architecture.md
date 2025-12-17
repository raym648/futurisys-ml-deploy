# Architecture du Système

## 🏗️ Vue d’ensemble

L’architecture du projet **Futurisys ML Deploy** 
repose sur une séparation claire et conforme 
aux bonnes pratiques **MLOps** entre :

* API (serving & orchestration)
* Couche Machine Learning (prédiction uniquement)
* Base de données (traçabilité)
* CI/CD (qualité & déploiement)
* Dashboard (monitoring & analyse)

Cette architecture est conçue pour être 
**testable, déployable automatiquement et auditable**.

---

## 🔌 Composants

### 🚀 API FastAPI

Rôle principal : **exposition du modèle ML en production**.

Fonctionnalités :

* Point d’entrée unique (`/`)
* Endpoint de prédiction (`/predict`)
* Registry de modèles (`/models`)
* Accès aux métadonnées (`/metadata`)
* Exposition des métriques (`/metrics`)
* Documentation Swagger automatique

👉 L’API ne contient **aucune logique d’entraînement ML**.

---

### 🧠 Couche Machine Learning

Responsabilité : **inférence uniquement**.

Caractéristiques :

* Chargement paresseux (lazy loading) des modèles
* Registry centralisé des modèles disponibles
* Modèle par défaut configurable
* Gestion des erreurs et fallback en cas de modèle invalide

Artefacts :

* Modèles sérialisés (`.joblib`)
* Fichiers de features et paramètres

👉 Aucun ré-entraînement en production.

---

### 🗄️ Base de données PostgreSQL (Neon)

Rôle : **traçabilité complète des prédictions**.

Stockage :

* Dataset source
* Inputs envoyés au modèle
* Outputs de prédiction
* Identifiants de requêtes

👉 Permet audit, monitoring et analyse a posteriori.

---

### 🔁 CI/CD – GitHub Actions

Pipeline automatisé exécuté à chaque `push` et `pull request`.

Étapes principales :

* Installation des dépendances
* Linting (flake8)
* Tests unitaires et fonctionnels (pytest)
* Smoke tests FastAPI
* Génération du rapport de couverture
* Déploiement automatique sur Hugging Face Spaces (branche `main`)

👉 En environnement CI (`ENV=test`), 
les modèles ML sont **mockés** pour garantir des tests rapides 
et reproductibles.

---

### 📊 Dashboard Streamlit

Fonctionnalités :

* Visualisation des métriques
* Analyse des prédictions
* Comparaison des modèles

👉 Connecté à l’API et/ou à la base de données.

---

## 🔄 Flux de données

1. Requête utilisateur vers l’API
2. Validation et préparation des features
3. Enregistrement de l’input en base
4. Prédiction via le modèle ML
5. Enregistrement de l’output en base
6. Réponse structurée à l’utilisateur

---

## 📌 Avantages de l’architecture

* ✅ Séparation claire des responsabilités
* ✅ Traçabilité complète des prédictions
* ✅ Tests CI indépendants des artefacts ML
* ✅ Scalabilité et maintenabilité
* ✅ Alignement avec les bonnes pratiques MLOps
