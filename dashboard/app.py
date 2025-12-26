# futurisys-ml-deploy/dashboard/app.py
# Streamlit dashboard connecté à l'API Futurisys ML

import os

import altair as alt
import pandas as pd
import requests
import streamlit as st

# from textwrap import dedent


# import time


# ============================================================
# API BASE URL
# ============================================================
API_BASE_URL = (
    (st.secrets.get("API_BASE_URL") or os.getenv("API_BASE_URL", ""))
    .strip()
    .rstrip("/")
)

if not API_BASE_URL:
    st.error(
        "API_BASE_URL is not configured. "
        "Please set it in Hugging Face Secrets or environment variables."
    )
    st.stop()

# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="Futurisys ML Dashboard",
    layout="wide",
)

st.title("📊 Futurisys ML – Monitoring & Inference Dashboard")


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🔎 Overview",
        "🧪 Metrics & Monitoring",
        "🧠 Model Comparison",
        "🤖 Submit Prediction Request",
        "🧾 Prediction History",
        "📚 Documentation API",
    ],
)


# ============================================================
# API HELPERS
# ============================================================
def api_get(path: str):
    r = requests.get(
        f"{API_BASE_URL}{path}",
        timeout=15,
        headers={"User-Agent": "futurisys-dashboard"},
    )
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict):
    r = requests.post(
        f"{API_BASE_URL}{path}",
        json=payload,
        timeout=15,
        headers={"User-Agent": "futurisys-dashboard"},
    )
    r.raise_for_status()
    return r.json()


# ============================================================
# OVERVIEW
# ============================================================
if page == "🔎 Overview":
    st.header("🔎 API Overview")

    metadata = api_get("/metadata/")
    models = api_get("/models/")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 API Metadata")
        st.json(metadata)

    with col2:
        st.subheader("🧠 Available Models")
        st.json(models)

# ============================================================
# METRICS & MONITORING
# ============================================================
elif page == "🧪 Metrics & Monitoring":
    st.header("🧪 Metrics & Monitoring")

    metrics = api_get("/metrics/summary")
    df = pd.DataFrame(metrics)

    if df.empty:
        st.warning("No metrics available.")
        st.stop()

    st.dataframe(df, use_container_width=True)

    if {"model", "pr_auc_mean"}.issubset(df.columns):
        st.subheader("📈 PR-AUC Mean per Model")

        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("model:N", title="Model"),
                y=alt.Y("pr_auc_mean:Q", title="PR-AUC Mean"),
                color="model:N",
                tooltip=list(df.columns),
            )
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Metrics format is incomplete.")

# ============================================================
# MODEL COMPARISON
# ============================================================
elif page == "🧠 Model Comparison":
    st.header("🧠 Model Comparison")

    metrics = api_get("/metrics/summary")
    df = pd.DataFrame(metrics)

    if df.empty or "model" not in df.columns:
        st.error("Invalid metrics format received from API.")
        st.stop()

    selected_models = st.multiselect(
        "Select models",
        options=df["model"].unique().tolist(),
        default=df["model"].unique().tolist(),
    )

    df_sel = df[df["model"].isin(selected_models)]

    metric = st.selectbox(
        "Metric",
        [c for c in df.columns if c != "model"],
    )

    chart = (
        alt.Chart(df_sel)
        .mark_bar()
        .encode(
            x=alt.X("model: N", title="Model"),
            y=alt.Y(f"{metric}: Q", title=metric),
            color="model:N",
            tooltip=list(df_sel.columns),
        )
    )

    st.altair_chart(chart, use_container_width=True)

# ============================================================
# PREDICTION HISTORY
# ============================================================
elif page == "🧾 Prediction History":
    st.header("🧾 Prediction History")

    history = api_get("/predictions/history")
    df = pd.DataFrame(history)

    if df.empty:
        st.info("No prediction history available.")
    else:
        st.dataframe(df, use_container_width=True)

# ============================================================
# SUBMIT PREDICTION REQUEST
# ============================================================
elif page == "🤖 Submit Prediction Request":
    st.header("🤖 Submit a Prediction Request")
    st.caption(
        "All prediction requests are stored in the database first. "
        "Inference is handled asynchronously by the backend."
    )

    models = api_get("/models/")
    available_models = models.get("available_models", [])
    default_model = models.get("default_model")

    if not available_models:
        st.error("❌ No model available from API.")
        st.stop()

    default_index = (
        available_models.index(default_model)
        if default_model in available_models
        else 0
    )

    model_name = st.selectbox(
        "Model",
        available_models,
        index=default_index,
    )

    with st.form("prediction_request_form"):
        age = st.number_input("Age", min_value=18, max_value=70, step=1)
        revenu = st.number_input(
            # fmt: off
            "Monthly income (€)", min_value=1.0, step=100.0
            # fmt: on
        )
        anciennete = st.number_input(
            # fmt: off
            "Years in company",
            min_value=0, step=1
            # fmt: on
        )
        frequence = st.selectbox(
            "Travel frequency",
            ["aucun", "occasionnel", "frequent"],
        )

        submitted = st.form_submit_button("Submit request")

    if submitted:
        payload = {
            "model_name": model_name,
            "source": "dashboard",
            "inputs": {
                "age": int(age),
                "revenu_mensuel": float(revenu),
                "annees_dans_l_entreprise": int(anciennete),
                "frequence_deplacement": frequence,
            },
        }

        result = api_post("/predictions/request", payload)

        request_id = result.get("request_id")
        status = result.get("status", "UNKNOWN")
        # fmt: off
        st.success("✅ Prediction request submitted")
        # fmt: on
        st.write(f"**Request ID: ** `{request_id}`")
        st.write(f"**Status: ** `{status}`")


# ============================================================
# DOCUMENTATION
# ============================================================
elif page == "📚 Documentation API":
    st.header("📚 Documentation API")

    st.markdown(
        f"""
    ### 📖 OpenAPI – Documentation interactive
-[Swagger UI]({API_BASE_URL}/docs)
-[ReDoc]({API_BASE_URL}/redoc)
    """
    )

    st.divider()

    st.subheader("📄 Documentation fonctionnelle & technique")

    DOCS_API_PAGES = {
        "📘 API": "api",
        "🏗️ Architecture": "architecture",
        "🧠 Model": "model",
        "📈 Monitoring": "monitoring",
        "🧪 Tests": "tests",
        "🔁 Update Policy": "update_policy",
    }

    doc_choice = st.selectbox(
        "Select documentation",
        list(DOCS_API_PAGES.keys()),
    )

    doc_key = DOCS_API_PAGES[doc_choice]

    try:
        # 🔗 Utilisation de l'abstraction API EXISTANTE
        doc_content = api_get(f"/docs/{doc_key}")

        # Le endpoint FastAPI renverra du Markdown brut
        st.markdown(doc_content["content"], unsafe_allow_html=True)

    except Exception as e:
        st.error("❌ Unable to load documentation from API")
        st.code(str(e))
