# futurisys-ml-deploy/dashboard/app.py
# Streamlit dashboard connecté à l'API Futurisys ML


import os

import altair as alt
import pandas as pd
import requests
import streamlit as st

# API_BASE_URL = st.secrets.get("API_BASE_URL") or os.getenv("API_BASE_URL")
API_BASE_URL = (
    (st.secrets.get("API_BASE_URL") or os.getenv("API_BASE_URL", ""))
    .strip()
    .rstrip("/")
)


if not API_BASE_URL:
    st.error(
        # fmt: off
        "API_BASE_URL is not configured."
        "Please set it in Hugging Face Secrets."
        # fmt: on
    )
    st.stop()


st.set_page_config(page_title="Futurisys ML Dashboard", layout="wide")

st.title("📊 Futurisys ML – Monitoring & Inference Dashboard")

# -----------------------------
# Sidebar navigation
# -----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "🔎 Overview",
        "🧪 Metrics & Monitoring",
        "🧠 Model Comparison",
        "🧾 Prediction History",
        "🤖 Predict",
    ],
)


# -----------------------------
# Helpers
# -----------------------------


def api_get(path: str):
    r = requests.get(f"{API_BASE_URL}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict):
    r = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


# -----------------------------
# Overview
# -----------------------------
if page == "🔎 Overview":
    st.header("🔎 API Overview")

    metadata = api_get("/metadata/")
    models = api_get("/models/")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Metadata")
        st.json(metadata)

    with col2:
        st.subheader("🧠 Available models")
        st.json(models)

# -----------------------------
# Metrics & Monitoring
# -----------------------------
elif page == "🧪 Metrics & Monitoring":
    st.header("🧪 Metrics & Monitoring")

    metrics = api_get("/metrics/")
    df = pd.DataFrame(metrics)

    st.dataframe(df)

    st.subheader("📈 Key metrics")

    if not df.empty:
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="model:N",
                y="roc_auc:Q",
                color="model:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)

# -----------------------------
# Model comparison
# -----------------------------
elif page == "🧠 Model Comparison":
    st.header("🧠 Model Comparison")

    metrics = api_get("/metrics/")
    df = pd.DataFrame(metrics)

    selected_models = st.multiselect(
        "Select models",
        options=df["model"].unique().tolist(),
        default=df["model"].unique().tolist(),
    )

    df_sel = df[df["model"].isin(selected_models)]

    metric = st.selectbox(
        "Metric", ["accuracy", "precision", "recall", "f1", "roc_auc"]
    )

    y_encoding = metric + ":Q"

    chart = (
        alt.Chart(df_sel)
        .mark_bar()
        .encode(
            x="model:N",  # noqa: E231
            y=y_encoding,
            color="model:N",  # noqa: E231
        )
    )

    st.altair_chart(chart, use_container_width=True)

# -----------------------------
# Prediction history
# -----------------------------
elif page == "🧾 Prediction History":
    st.header("🧾 Prediction History")

    history = api_get("/dataset/")
    df = pd.DataFrame(history)

    st.dataframe(df)

# -----------------------------
# Prediction
# -----------------------------
elif page == "🤖 Predict":
    st.header("🤖 Make a prediction")

    models = api_get("/models/")
    model_name = st.selectbox(
        "Model",
        models.get("available", []),
        index=models.get("default_index", 0),
    )

    with st.form("predict_form"):
        id_employee = st.number_input("Employee ID", step=1)
        age = st.number_input("Age", step=1)
        revenu = st.number_input("Monthly income", step=100)

        submitted = st.form_submit_button("Predict")

    if submitted:
        payload = {
            "id_employee": id_employee,
            "age": age,
            "revenu_mensuel": revenu,
            "model": model_name,
        }

        result = api_post("/predict/", payload)

        st.success("Prediction completed")
        st.json(result)
