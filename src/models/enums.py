# futurisys-ml-deploy/src/models/enums.py

import enum


class PredictionStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
