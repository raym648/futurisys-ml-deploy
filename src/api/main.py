# futurisys-ml-deploy/src/api/main.py

from fastapi import FastAPI

from src.api.routes.dataset import router as dataset_router
from src.api.routes.docs_api import router as docs_router  # 👈 NOUVEAU
from src.api.routes.metadata import router as metadata_router
from src.api.routes.metrics import router as metrics_router
from src.api.routes.models import router as models_router
from src.api.routes.predictions import router as predictions_router

app = FastAPI(
    title="Futurisys ML API",
    description="API MLOps – Dataset, Prediction & Artefacts",
    version="1.1.0",
)

# ============================================================
# Routes datasets
# ============================================================

app.include_router(dataset_router)

# ============================================================
# Routes ML prediction
# ============================================================

app.include_router(predictions_router)

# ============================================================
# Routes metadata (artefacts)
# ============================================================

app.include_router(metadata_router)

# ============================================================
# Routes models registry
# ============================================================

app.include_router(models_router)

# ============================================================
# Routes metrics
# ============================================================

app.include_router(metrics_router)

# ============================================================
# Routes documentation
# ============================================================

app.include_router(docs_router)

# ============================================================
# Root / health
# ============================================================


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "futurisys-ml-api"}
