---
title: Futurisys Dashboard
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
  - streamlit
  - machine-learning
  - mlops
  - dashboard
pinned: false
short_description: Dashboard Streamlit pour le monitoring MLOps
---

# 🚀 Futurisys ML – Hugging Face Space

This Space provides a **production‑ready MLOps dashboard** connected to a FastAPI backend.

---

## 🔎 Features

### 📦 Metadata

* Dataset version
* Feature count
* Training configuration

### 🧠 Models

* List of deployed models
* Default production model (`random_forest_e04`)

### 🧪 Metrics & Monitoring

* Accuracy, Precision, Recall, F1, ROC‑AUC
* Visual comparison across models

### 🧠 Model comparison

* Interactive selection of models
* Metric‑wise bar charts

### 🧾 Prediction history

* Historical predictions from database
* Traceability (request_id, model, timestamp)

### 🤖 Live prediction

* Form‑based inference
* Model selection
* Probability & class output

---

## 🏗 Architecture

```
FastAPI (API)
 ├── /metadata
 ├── /models
 ├── /metrics
 ├── /dataset
 └── /predict
        ↑
        │
Streamlit Dashboard (this Space)
```

---

## ⚙️ Configuration

### Environment variables

| Variable       | Description      |
| -------------- | ---------------- |
| `API_BASE_URL` | FastAPI base URL |

Configured via **Hugging Face Space → Settings → Secrets**.
```
API_BASE_URL=https://<ton-api-fastapi>
```

Exemple :
- local : http://localhost:8000
- prod : https://futurisys-ml-api.hf.space

---

## 🚦 CI/CD

* GitHub Actions
* Automatic deployment on `main`
* Artifacts synced from `/src`

---

## 🧠 Default production model

```
random_forest_e04
```

Promoted after cross‑validation & SMOTE balancing.

---

## ✅ Status

✔ MLOps ready
✔ Traceable predictions
✔ Model governance

---

Maintained by **Futurisys – AI Engineer Program**
