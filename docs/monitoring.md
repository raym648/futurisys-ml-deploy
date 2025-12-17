# Monitoring & Observabilité

## 🎯 Objectifs

Le monitoring vise à garantir :

* la fiabilité des prédictions en production
* la détection précoce des dérives (data drift & concept drift)
* la transparence des performances du modèle
* la traçabilité des décisions ML

---

## 📊 Métriques suivies

Les métriques sont calculées hors‑ligne après entraînement et comparées entre versions de modèles :

* Accuracy
* Precision
* Recall
* F1‑score
* Matrice de confusion
* Distribution des prédictions (classe 0 / classe 1)

Chaque fichier de métriques est versionné par modèle.

---

## 🗄️ Stockage des métriques

* Calculées offline (notebook / pipeline ML)
* Stockées sous forme de fichiers CSV
* Localisation : `data/ml_artifacts/metrics/`
* Un fichier CSV par modèle et par version

Les métriques sont exposées via l’API REST :

* `GET /metrics` → liste des fichiers disponibles
* `GET /metrics/{filename}` → contenu détaillé d’un fichier

---

## 📈 Dashboard

Le dashboard Streamlit permet :

* la visualisation des performances par modèle
* la comparaison entre versions
* l’analyse temporelle des résultats
* l’aide à la décision pour la promotion d’un modèle en production

---

## 🔍 Observabilité applicative

En complément des métriques ML :

* chaque requête est tracée (input / output)
* les prédictions sont historisées en base de données
* les erreurs sont visibles via les logs applicatifs

---

## 🚨 Perspectives d’amélioration

* Ajout d’alertes automatiques (seuils de performance)
* Détection automatique de data drift
* Centralisation des logs (ex : OpenTelemetry)
* Monitoring en temps réel des distributions d’inputs
