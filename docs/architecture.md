# Architecture du Système

## 🏗️ Vue d’ensemble

L’architecture repose sur une séparation claire entre :

* API
* Modèle ML
* Base de données
* CI/CD
* Dashboard

---

## 🔌 Composants

### API FastAPI

* Point d’entrée unique
* Gestion des requêtes de prédiction
* Exposition Swagger

### Base PostgreSQL (Neon)

* Dataset
* Inputs du modèle
* Outputs du modèle

### Couche ML

* Artefacts versionnés
* Aucun entraînement en production

### CI/CD

* GitHub Actions
* Tests, lint, déploiement

### Dashboard Streamlit

* Visualisation des métriques
* Comparaison de modèles

---

## 🔄 Flux de données

1. Requête API
2. Enregistrement input
3. Prédiction ML
4. Enregistrement output
5. Réponse utilisateur

---

## 📌 Avantages

* Traçabilité
* Scalabilité
* Robustesse
* Lisibilité
