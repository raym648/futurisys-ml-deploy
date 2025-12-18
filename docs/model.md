# Documentation du Modèle de Machine Learning

## 🧠 Description générale

Le modèle implémente une **classification binaire** visant à prédire un comportement cible à partir de variables socio‑professionnelles.

---

## ⚙️ Choix techniques

* **Algorithme** : RandomForestClassifier

* **Justification** :

  * robustesse aux données bruitées
  * bonne interprétabilité
  * performances stables

* **Gestion du déséquilibre** : SMOTE

---

## 📦 Artefacts

* Modèle final : `e04_random_forest_final.joblib`
* Pipeline : `e04_rf_smote_pipeline.joblib`
* Features : `e02_all_features_final_list.joblib`
* Jeux de données : `.npy`, `.csv`

---

## 📊 Performances

Les métriques sont issues de validations croisées et de jeux de test :

* Accuracy
* Precision
* Recall
* F1‑score

Les résultats détaillés sont stockés dans des fichiers CSV et exposés via l’API `/metrics`.

---

## 🔁 Utilisation en production

* Chargement du modèle au démarrage
* Aucune phase de ré‑entraînement côté API
* Sélection dynamique du modèle via le registry

---

## 🛠️ Maintenance

* Mise à jour des modèles par versionnement des artefacts
* Tests automatisés avant déploiement
* Traçabilité complète via PostgreSQL
