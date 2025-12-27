# 🏗️ Architecture – Futurisys ML Deploy

## 1. Objectif du document

Ce document décrit l’architecture technique complète du projet **Futurisys ML Deploy**. Il sert de référence unique pour :

* Comprendre l’organisation globale du système
* Justifier les choix MLOps (Projet-5)
* Faciliter la maintenance, les tests et l’évolution
* Appuyer la soutenance orale et l’évaluation

L’architecture suit une approche **DB-first**, **asynchrone**, et **découplée**, conforme aux bonnes pratiques MLOps.

---

## 2. Vue d’ensemble

L’architecture est composée de cinq briques principales :

1. **Dashboard (Streamlit)** – Interface utilisateur
2. **API (FastAPI)** – Orchestration et exposition REST
3. **Base de données (PostgreSQL – Neon)** – Source de vérité
4. **Worker asynchrone** – Inférence ML hors API
5. **ML Model Registry** – Gestion centralisée des modèles

```mermaid
flowchart LR
    UI[Dashboard<br/>(Streamlit)]
    API[FastAPI API]
    DB[(PostgreSQL<br/>Neon)]
    WORKER[Async Worker]
    REGISTRY[ML Model Registry]

    UI -->|REST| API
    API -->|INSERT / SELECT| DB
    WORKER -->|SELECT PENDING| DB
    WORKER -->|UPDATE / INSERT| DB
    WORKER -->|load model| REGISTRY
```

---

## 3. Dashboard (Streamlit)

**Rôle :**

* Interface utilisateur
* Soumission de requêtes de prédiction
* Visualisation des métriques
* Consultation de l’historique des prédictions

**Caractéristiques :**

* Ne contient aucune logique ML
* Consomme exclusivement l’API FastAPI
* Stateless (aucune donnée persistée localement)

**Endpoints consommés :**

* `GET /metadata/`
* `GET /models/`
* `POST /predictions/request`
* `GET /predictions/{request_id}`
* `GET /predictions/history`

---

## 4. API FastAPI

**Rôle :**

* Exposition des endpoints REST
* Validation des entrées
* Accès contrôlé à la base de données
* Aucun calcul ML direct

**Fichier principal :**

* `src/api/main.py`

### 4.1 Routes principales

| Route            | Responsabilité                    |
| ---------------- | --------------------------------- |
| `/predictions/*` | Gestion des requêtes et résultats |
| `/models`        | Liste des modèles disponibles     |
| `/metadata`      | Métadonnées ML                    |
| `/metrics`       | Indicateurs de performance        |
| `/docs`          | Documentation exposée             |

### 4.2 Principe DB-first

Lorsqu’une requête de prédiction est soumise :

1. L’API **enregistre la requête en base**
2. Le statut est positionné à `PENDING`
3. Aucune inférence n’est exécutée côté API

Ce choix garantit :

* Scalabilité
* Résilience
* Découplage fort API / ML

---

## 5. Base de données (PostgreSQL)

La base de données constitue la **source de vérité métier**.

### 5.1 Tables principales

#### `prediction_requests`

| Champ        | Description                  |
| ------------ | ---------------------------- |
| `id`         | Clé primaire (DB)            |
| `request_id` | UUID métier exposé           |
| `model_name` | Modèle demandé               |
| `status`     | pending / completed / failed |
| `created_at` | Date de création             |
| features     | Données d’entrée ML          |

#### `prediction_results`

| Champ         | Description                    |
| ------------- | ------------------------------ |
| `id`          | Clé primaire                   |
| `request_id`  | FK vers prediction_requests.id |
| `prediction`  | Classe prédite                 |
| `probability` | Probabilité                    |
| `created_at`  | Date du calcul                 |

Relation : **1–1 stricte**

---

## 6. Worker asynchrone

**Fichier :** `src/workers/prediction_worker.py`

**Rôle :**

* Polling périodique de la base
* Traitement des requêtes `PENDING`
* Exécution de l’inférence ML
* Mise à jour des résultats

**Boucle de fonctionnement :**

1. Lecture des requêtes `PENDING`
2. Chargement du modèle via le registry
3. Exécution de `run_inference`
4. Insertion dans `prediction_results`
5. Mise à jour du statut

Le worker est **totalement indépendant de l’API**.

---

## 7. ML Model Registry

**Fichiers :**

* `src/ml/model_registry.py`
* `src/ml/artifacts.py`

**Objectif :**
Fournir un **point d’accès unique** aux artefacts ML.

### 7.1 Responsabilités

* Chargement lazy des modèles
* Gestion des features
* Accès aux métadonnées
* Mock automatique en environnement `test`

### 7.2 Modèles disponibles

* dummy
* logistic
* random_forest
* random_forest_e04 (défaut)

Le registry empêche toute duplication de logique ML dans l’API ou le worker.

---

## 8. Gestion des environnements

| Environnement | Comportement                    |
| ------------- | ------------------------------- |
| `prod`        | Chargement réel des artefacts   |
| `test`        | Modèles mockés, pas de fichiers |

Cela garantit :

* Tests CI rapides
* Déploiements fiables

---

## 9. Sécurité & robustesse

* Pas d’exécution ML dans l’API
* Transactions DB protégées
* Rollback en cas d’erreur
* Typage strict ORM + Pydantic

---

## 10. Alignement avec le Projet-5 (MLOps)

Cette architecture valide pleinement les attendus :

* Séparation claire des responsabilités
* Déploiement d’un modèle ML via API
* Monitoring et historique
* Tests automatisables
* Architecture évolutive

---

## 11. Perspectives d’évolution

* Ajout d’une file de messages (Redis / RabbitMQ)
* Worker multi-process
* Authentification API
* Versioning avancé des modèles

---

## 12. CI/CD – GitHub Actions

Le projet **Futurisys ML Deploy** intègre une chaîne **CI/CD complète** basée sur **GitHub Actions**, exécutée automatiquement à chaque `push` et `pull request` sur les branches `dev` et `main`.

### 🎯 Objectifs du pipeline

* Garantir la qualité du code
* Détecter les régressions fonctionnelles
* Valider l’API sans dépendance aux artefacts ML réels
* Automatiser le déploiement en production

### ⚙️ Étapes principales du pipeline

1. Installation des dépendances (via `requirements.txt`)
2. Linting avec `flake8`
3. Tests unitaires et fonctionnels avec `pytest`
4. Smoke tests FastAPI (vérification des endpoints critiques)
5. Génération du rapport de couverture
6. Déploiement automatique sur Hugging Face Spaces (branche `main`)

### 🧪 Mode CI / Tests (`ENV=test`)

En environnement CI :

* La variable d’environnement `ENV=test` est définie
* Les modèles ML sont **mockés** via `model_registry.py`
* Aucun fichier `.joblib` réel n’est chargé
* Les tests sont **rapides, déterministes et reproductibles**

👉 Cette stratégie permet de tester l’API, la base de données et les workers **sans dépendance aux artefacts ML**, tout en conservant une couverture fonctionnelle élevée.

---

**Document de référence – Futurisys ML Deploy**
