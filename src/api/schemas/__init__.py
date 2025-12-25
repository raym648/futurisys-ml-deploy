# futurisys-ml-deploy/src/api/schemas/__init__.py

from .enums import FrequenceDeplacement
from .input import PredictionInput
from .output import PredictionRequestResponse, PredictionResultResponse

__all__ = [
    "PredictionInput",
    "PredictionRequestResponse",
    "PredictionResultResponse",
    "FrequenceDeplacement",
]
