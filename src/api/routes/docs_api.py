# futurisys-ml-deploy/src/api/routes/docs_api.py
# Routes API pour exposer la documentation Markdown via OpenAPI

from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/docs",
    tags=["documentation"],
)

# ============================================================
# Configuration
# ============================================================

DOCS_BASE_PATH = Path(__file__).resolve().parents[3] / "docs"

ALLOWED_DOCS = {
    "api": "api.md",
    "architecture": "architecture.md",
    "model": "model.md",
    "monitoring": "monitoring.md",
    "tests": "tests.md",
    "update_policy": "update_policy.md",
}

# ============================================================
# Routes
# ============================================================


@router.get("/{doc_name}", summary="Get API documentation (Markdown)")
def get_documentation(doc_name: str):
    """
    Retrieve a Markdown documentation file.

    - **doc_name**: Name of the documentation
      (api, architecture, model, monitoring, tests, update_policy)
    """

    if doc_name not in ALLOWED_DOCS:
        raise HTTPException(
            status_code=404,
            detail=f"Documentation '{doc_name}' not found",
        )

    doc_file = DOCS_BASE_PATH / ALLOWED_DOCS[doc_name]

    if not doc_file.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Documentation file missing: {doc_file.name}",
        )

    return {
        "name": doc_name,
        "content": doc_file.read_text(encoding="utf-8"),
    }
