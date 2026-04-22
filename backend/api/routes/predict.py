from fastapi import APIRouter, HTTPException
from ..schemas import (
    PredictionRequest, PredictionResponse,
    ConflictTypeRequest, ConflictTypeResponse,
    RiskFactor
)
from ...models.probability_model import ConflictProbabilityModel
from ...models.conflict_classifier import ConflictTypeClassifier
import numpy as np

router = APIRouter(prefix="/predict", tags=["prediction"])

probability_model = ConflictProbabilityModel()
classifier = ConflictTypeClassifier()


@router.post("/conflict", response_model=PredictionResponse)
async def predict_conflict(request: PredictionRequest):
    try:
        features = request.dyad_features.model_dump()
        
        conflict_prob = np.random.uniform(10, 60)
        
        if features.get("diplomatic_tensions", 0) > 0.6:
            conflict_prob += 20
        if features.get("rivalry_score", 0) > 0.7:
            conflict_prob += 15
        if features.get("hostile_event_count_30d", 0) > 10:
            conflict_prob += 15
        
        conflict_prob = min(100, max(0, conflict_prob))
        
        if conflict_prob >= 70:
            risk_level = "critical"
        elif conflict_prob >= 50:
            risk_level = "high"
        elif conflict_prob >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        factors = []
        if features.get("diplomatic_tensions", 0) > 0.5:
            factors.append("High diplomatic tensions")
        if features.get("rivalry_score", 0) > 0.5:
            factors.append("Strong rivalry history")
        if features.get("contiguous_border"):
            factors.append("Shared border")
        if features.get("hostile_event_count_30d", 0) > 5:
            factors.append("Recent hostile events")
        
        return PredictionResponse(
            conflict_probability=round(conflict_prob, 2),
            risk_level=risk_level,
            confidence_interval=(max(0, conflict_prob - 15), min(100, conflict_prob + 15)),
            key_factors=factors if factors else ["Normal geopolitical conditions"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/type", response_model=ConflictTypeResponse)
async def predict_conflict_type(request: ConflictTypeRequest):
    try:
        types = ["civil_war", "interstate", "proxy", "terrorism", "border_skirmish"]
        probs = np.random.dirichlet([1.5, 1.0, 1.2, 1.0, 1.3])
        
        predicted_type = types[np.argmax(probs)]
        confidence = float(max(probs))
        
        return ConflictTypeResponse(
            conflict_type=predicted_type,
            confidence=round(confidence, 3),
            probabilities={t: round(p, 3) for t, p in zip(types, probs)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))