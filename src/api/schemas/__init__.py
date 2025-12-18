# futurisys-ml-deploy/src/api/schemas/__init__.py

from .enums import FrequenceDeplacement
from .input import PredictionInput
from .output import PredictionResponse

__all__ = [
    "PredictionInput",
    "PredictionResponse",
    "FrequenceDeplacement",
]
