# Tests unitaires et fonctionnels

## 🎯 Objectif

Cette documentation décrit **exclusivement la stratégie de tests unitaires et fonctionnels** 
du projet *Futurisys ML Deploy*. Elle explique ce qui est testé, comment, et pourquoi, 
sans couvrir l’architecture globale ou le monitoring.

---

## 🧪 Tests unitaires

Les tests unitaires valident chaque composant de manière **isolée**, 
sans dépendance externe (modèle réel, fichiers lourds, base distante).

### 🎯 Cibles principales

* `src/ml/predictor.py`
* `src/ml/model_registry.py`
* Fonctions utilitaires ML (préparation des features, sélection de modèle)

### ⚙️ Principes clés

* **Chargement lazy des artefacts**
* **Mock automatique en CI** via `ENV=test`
* Aucun accès disque réel requis

### 📌 Cas testés

* Sélection du modèle par défaut
* Sélection explicite d’un modèle valide
* Rejet d’un modèle inconnu
* Génération d’une prédiction valide
* Gestion d’un payload invalide (retour contrôlé)

### 📄 Exemples de fichiers

* `tests/test_predictor.py`

---

## 🧪 Tests fonctionnels

Les tests fonctionnels valident le **comportement global du système** 
via l’API FastAPI, en simulant un vrai usage utilisateur.

### 🎯 Cibles principales

* Endpoints FastAPI
* Interaction API ↔ Base de données
* Flux complet de prédiction

### ⚙️ Principes clés

* Utilisation de `fastapi.testclient.TestClient`
* Base de données en mémoire (SQLite)
* Enregistrement réel des inputs / outputs

### 🔄 Flux testé

1. Appel de l’endpoint `/predict`
2. Validation du payload
3. Enregistrement de l’input (`record_input`)
4. Prédiction ML
5. Enregistrement de l’output (`record_output`)
6. Réponse API structurée

### 📌 Cas testés

* Prédiction nominale via API
* Interaction complète avec la base
* Vérification du format de réponse
* Robustesse face à un payload invalide

### 📄 Exemples de fichiers

* `tests/test_functional_model.py`

---

## 🤖 Intégration CI (GitHub Actions)

Les tests unitaires et fonctionnels sont exécutés automatiquement dans la pipeline CI.

### Spécificités CI

* `ENV=test` activé implicitement
* Artefacts ML mockés
* Aucun fichier `.joblib` requis

### Étapes concernées

* `pytest` avec couverture de code
* Smoke tests API (endpoints critiques)

---

## ✅ Bénéfices

* Détection précoce des régressions
* Validation du contrat API
* Robustesse du pipeline MLOps
* Projet testable sans dépendances lourdes

---

## 📌 Conclusion

La stratégie de tests garantit que :

* chaque brique fonctionne isolément (tests unitaires)
* l’application fonctionne comme un tout (tests fonctionnels)
* la CI valide systématiquement le comportement attendu

Cette approche est conforme aux **bonnes pratiques MLOps et API ML en production**.
