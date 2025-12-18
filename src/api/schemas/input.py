# futurisys-ml-deploy/src/api/schemas/input.py

from pydantic import BaseModel, ConfigDict, Field

from .enums import FrequenceDeplacement


class PredictionInput(BaseModel):
    """
    Schéma d'entrée pour la prédiction ML.
    Strictement aligné avec les features utilisées à l'entraînement.
    """

    age: int = Field(
        ...,
        ge=18,
        le=70,
        description="Âge du salarié",
    )
    revenu_mensuel: float = Field(
        ...,
        gt=0,
        description="Revenu mensuel en euros",
    )
    annees_dans_l_entreprise: int = Field(
        ...,
        ge=0,
        description="Ancienneté dans l'entreprise",
    )
    frequence_deplacement: FrequenceDeplacement

    # ✅ Pydantic v2 (remplace class Config + schema_extra)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 30,
                "revenu_mensuel": 5000,
                "annees_dans_l_entreprise": 5,
                "frequence_deplacement": "occasionnel",
            }
        }
    )
