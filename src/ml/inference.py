# futurisys-ml-deploy/src/ml/inference.py

import pandas as pd

from src.ml.model_registry import get_model


def run_inference(payload: dict) -> tuple[int, float]:
    """
    Inference synchrone.
    Le modèle embarque son propre pipeline de features.
    """
    model = get_model()  # modèle par défaut

    # On passe les features BRUTES
    df = pd.DataFrame([payload])

    proba = model.predict_proba(df)[0][1]
    pred = int(proba >= 0.5)

    return pred, float(proba)
