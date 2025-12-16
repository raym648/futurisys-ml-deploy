# Étape 4 — Intégration du Dataset et Gestion des Données via PostgreSQL

Ce document décrit de manière contextualisée l’intégration de l’étape 4 dans la documentation du projet. Il explicite les choix techniques, les workflows API → DB → Modèle et fournit des exemples d’interactions adaptés à la mission du **Projet‑4 — « Classifiez automatiquement des informations »** (analyse d’attrition pour TechNova Partners).

---

## 1. Contexte métier et portée

TechNova Partners (ESN) souhaite comprendre les causes d’attrition en s’appuyant sur trois sources de données :

1. Extrait SIRH (données RH : poste, ancienneté, salaire, âge, code fonction, etc.),
2. Extrait évaluations de performance (notes, remarques, satisfaction),
3. Extrait sondage bien‑être (réponses au questionnaire annuel + témoin `left_company`).

L’objectif technique de l’étape 4 est d’ingérer ces trois sources dans PostgreSQL, d’assurer leur traçabilité et de centraliser **toutes** les interactions avec le modèle de classification (inputs & outputs) afin d’autoriser audits, analyses post‑hoc et réentraînements.

---

## 2. Choix techniques — justification courte

* **PostgreSQL (Neon Serverless)** : stockage relationnel robuste, support JSONB pour champs semi‑structurés et scalabilité serverless.
* **SQLAlchemy** : définition claire des modèles, facilité de maintenance et compatibilité Alembic pour les migrations.
* **Psycopg 3** : driver moderne et performant, compatible async si nécessaire.
* **Schéma séparé** : tables distinctes pour `dataset_*` (sources), `model_inputs`, `model_outputs`, `model_versions`, `audit_log`.
* **Rôles SQL** (`app_writer`, `app_reader`) : principe du moindre privilège pour protéger les données RH.

---

### Choix architectural
Le dataset est stocké sous forme de documents JSONB afin de garantir :

- une flexibilité maximale du schéma,
- une compatibilité avec l’évolution des features,
- une traçabilité complète des données utilisées par le modèle.

---

## 3. Schéma conceptuel adapté au projet‑4

Les tables clés :

* `dataset_sirh` — colonnes issues du SIRH (employee_id PK, age, salary, role, tenure, etc.)
* `dataset_perf` — évaluations (employee_id FK, year, performance_score, satisfaction_score)
* `dataset_survey` — réponses sondage (employee_id FK, question_1..N, left_company BOOLEAN)
* `model_inputs` — (input_id PK, request_id UUID, employee_id, payload JSONB, model_version, created_at, status)
* `model_outputs` — (output_id PK, input_id FK, request_id UUID, prediction JSONB, explanation JSONB (ex: SHAP summary), metrics JSONB, created_at)
* `model_versions` — versioning du pipeline/model (git_hash, package_versions, notes)
* `audit_log` — traces d’opérations critiques (erreurs, rollbacks, policy events)

Chaque table porte des index sur `employee_id`, `request_id` et `created_at` pour accélérer analyses et audits.

---

