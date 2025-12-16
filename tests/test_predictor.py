# futurisys-ml-deploy/tests/test_predictor.py

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

from src.ml.artifacts import MODELS, default_model
from src.ml.predictor import get_model, predict, prepare_features

BASE_DIR01 = Path("futurisys-ml-deploy/data/processed/")
BASE_DIR02 = Path("futurisys-ml-deploy/data/ml_artifacts/")
BASE_DIR03 = Path("futurisys-ml-deploy/data/ml_artifacts/models/")


@pytest.fixture
def load_data():
    df = pd.read_csv(BASE_DIR01 / "e01_df_central_left_clean.csv")
    X_train = np.load(BASE_DIR02 / "e02_X_train_final.npy")
    X_test = np.load(BASE_DIR02 / "e02_X_test_final.npy")
    return df, X_train, X_test


@pytest.fixture
def load_model():
    return joblib.load(BASE_DIR03 / "e04_random_forest_final.joblib")


def test_prepare_features_with_real_data(load_data):
    df, _, _ = load_data
    payload = df.iloc[0].to_dict()
    result = prepare_features(payload)

    assert result.shape == (1, len(payload))
    assert isinstance(result, np.ndarray)


def test_get_model_default():
    model = get_model()
    assert model == default_model


def test_get_model_valid():
    model = get_model("logistic")
    assert model in MODELS.values()


def test_get_model_invalid():
    with pytest.raises(ValueError):
        get_model("invalid_model")


def test_predict_with_real_data(load_data, load_model):
    df, _, _ = load_data
    payload = df.iloc[0].to_dict()

    result = predict(payload, model_name="random_forest")

    assert "prediction" in result
    assert "probability" in result
    assert isinstance(result["probability"], float)
    assert result["prediction"] in [0, 1]
