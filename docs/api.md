# Documentation de l’API – FastAPI

## 🎯 Objectif

Cette API expose un modèle de Machine Learning de classification et fournit des endpoints pour la prédiction, la consultation des modèles, des métriques et des métadonnées.

---

## 🔗 Base URL

```
http://<host>:<port>
```

---

## 📌 Endpoints

### `/predict`

**Méthode** : POST

Permet d’obtenir une prédiction à partir d’un payload JSON.

**Exemple de requête** :

```json
{
  "age": 42,
  "revenu_mensuel": 3200
}
```

**Réponse** :

```json
{
  "prediction": 1,
  "probability": 0.87
}
```

Chaque requête est enregistrée en base (input + output).

---

### `/models`

**Méthode** : GET

Retourne la liste des modèles disponibles et le modèle par défaut.

---

### `/metadata`

**Méthode** : GET

Fournit les informations générales du projet : version, auteur, description.

---

### `/metrics`

**Méthode** : GET

Expose les métriques de performance du modèle (accuracy, recall, etc.).

---

## 📖 Documentation interactive

La documentation Swagger est accessible automatiquement via :

* `/docs`
* `/redoc`

Ces pages sont générées grâce à OpenAPI (FastAPI).
