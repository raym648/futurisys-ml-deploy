# Tests unitaires, de schémas et fonctionnels

## 🎯 Objectif

Cette documentation décrit **exclusivement la stratégie de tests unitaires, de validation des schémas et de tests fonctionnels**
du projet *Futurisys ML Deploy*. Elle explique **ce qui est testé, comment, et pourquoi**,
sans couvrir l’architecture globale ni le monitoring.

L’objectif est de garantir :

* la fiabilité de la logique ML,
* la robustesse de la validation des données,
* le bon fonctionnement de l’API exposée.

---

## 🧪 Tests unitaires (logique ML)

Les tests unitaires valident chaque composant de manière **isolée**,
sans dépendance externe (API FastAPI, base de données, artefacts lourds).

### 🎯 Cibles principales

* `src/ml/predictor.py`
* `src/ml/model_registry.py`
* Fonctions utilitaires ML (préparation des features, sélection de modèle)

### ⚙️ Principes clés

* **Isolation complète de la logique métier ML**
* Chargement **lazy** des modèles
* Aucun serveur API requis
* Aucun accès disque obligatoire

### 📌 Cas testés

* Sélection du modèle par défaut
* Sélection explicite d’un modèle valide
* Rejet d’un modèle inconnu
* Reconstruction correcte du vecteur de features
* Génération d’une prédiction valide
* Gestion contrôlée des erreurs ML

### 📄 Fichiers concernés

* `tests/unit/test_predictor.py`

---

## 📐 Tests de schémas (validation des données)

Les tests de schémas vérifient la **validation stricte des entrées utilisateur**
via Pydantic, indépendamment de l’API et du modèle ML.

### 🎯 Cibles principales

* Schémas Pydantic (`PredictionInput`, Enums)
* Contraintes de types et de valeurs

### ⚙️ Principes clés

* Validation exécutée **avant toute logique métier**
* Rejet automatique des données invalides (`HTTP 422`)
* Source de vérité alignée avec le dataset `.csv`

### 📌 Cas testés

* Payload valide
* Valeur Enum invalide
* Champ manquant
* Type incorrect

### 📄 Fichiers concernés

* `tests/schemas/test_schemas_input.py`

---

## 🌐 Tests fonctionnels (API FastAPI)

Les tests fonctionnels valident le **comportement global de l’application**
via l’API FastAPI, en simulant un usage réel.

### 🎯 Cibles principales

* Endpoints FastAPI
* Intégration API ↔ couche ML
* Gestion des erreurs HTTP

### ⚙️ Principes clés

* Utilisation de `fastapi.testclient.TestClient`
* Base de données neutralisée via mocks
* Aucun modèle réel requis

### 🔄 Flux testé

1. Appel de l’endpoint `/predict`
2. Validation du payload (Pydantic)
3. Appel de la couche ML (`predictor`)
4. Génération de la prédiction
5. Réponse API structurée

### 📌 Cas testés

* Prédiction nominale via API
* Modèle invalide (erreur contrôlée)
* Format de réponse conforme au contrat API
* Robustesse face à un payload invalide

### 📄 Fichiers concernés

* `tests/functional/test_functional_model.py`

---

## 🤖 Intégration CI (GitHub Actions)

Les tests sont exécutés automatiquement et **séparément** dans la pipeline CI.

### Étapes CI

* Tests unitaires ML
* Tests de schémas Pydantic
* Tests fonctionnels API
* Rapport de couverture de code
* Smoke tests FastAPI

### Spécificités CI

* `ENV=test` activé
* Artefacts ML mockés
* Aucune dépendance externe requise

---

## ✅ Bénéfices

* Séparation claire des responsabilités
* Détection précoce des régressions
* Validation stricte du contrat API
* Pipeline CI fiable et reproductible

---

## 📌 Conclusion

La stratégie de tests garantit que :

* la logique ML est fiable et testée isolément,
* les données d’entrée sont strictement validées,
* l’API se comporte correctement en conditions réelles,
* chaque couche peut évoluer indépendamment.

Cette approche est conforme aux **bonnes pratiques MLOps et API ML en production**.
