# futurisys-ml-deploy/src/api/schemas/enums.py

from enum import Enum


class FrequenceDeplacement(str, Enum):
    """
    Enum strictement dérivé du dataset d'entraînement (.csv).
    """

    aucun = "aucun"
    occasionnel = "occasionnel"
    frequent = "frequent"
