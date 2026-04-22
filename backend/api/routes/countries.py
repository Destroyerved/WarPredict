from fastapi import APIRouter, HTTPException
from ..schemas import CountryProfile, RiskFactor
from ...utils.feature_engineering import create_country_features
import numpy as np
import random

router = APIRouter(prefix="/countries", tags=["countries"])

COUNTRY_NAMES = {
    "USA": "United States", "CHN": "China", "RUS": "Russia", "IND": "India",
    "PAK": "Pakistan", "IRN": "Iran", "ISR": "Israel", "TUR": "Turkey",
    "DEU": "Germany", "GBR": "United Kingdom", "FRA": "France", "BRA": "Brazil",
    "JPN": "Japan", "KOR": "South Korea", "NGA": "Nigeria", "EGY": "Egypt",
    "SAU": "Saudi Arabia", "UKR": "Ukraine", "VEN": "Venezuela", "SYR": "Syria",
    "PRK": "North Korea", "AUS": "Australia", "CAN": "Canada", "MEX": "Mexico"
}


@router.get("")
async def get_countries():
    return {"countries": list(COUNTRY_NAMES.keys())}


@router.get("/{country_code}", response_model=CountryProfile)
async def get_country_profile(country_code: str):
    if country_code not in COUNTRY_NAMES:
        raise HTTPException(status_code=404, detail="Country not found")
    
    features = create_country_features(2024, country_code, None)
    
    base_risk = np.random.uniform(10, 40)
    if features.get("political_instability_index", 50) > 70:
        base_risk += 25
    if features.get("past_conflict_count_10yr", 0) > 2:
        base_risk += 15
    
    risk_score = min(100, max(0, base_risk))
    
    return CountryProfile(
        code=country_code,
        name=COUNTRY_NAMES[country_code],
        gdp=random.uniform(1e12, 25e12),
        population=random.uniform(1e6, 1.5e9),
        military_expenditure=random.uniform(1, 6),
        stability_score=100 - features["political_instability_index"],
        nuclear_capable=features["nuclear_capable"],
        recent_conflicts=features["past_conflict_count_10yr"],
        risk_score=round(risk_score, 1)
    )


@router.get("/{country_code}/risk-factors")
async def get_risk_factors(country_code: str):
    if country_code not in COUNTRY_NAMES:
        raise HTTPException(status_code=404, detail="Country not found")
    
    factors = [
        RiskFactor(factor="Political instability", contribution=0.35, direction="positive"),
        RiskFactor(factor="Rivalry with neighbors", contribution=0.25, direction="positive"),
        RiskFactor(factor="Recent hostile events", contribution=0.20, direction="positive"),
        RiskFactor(factor="Economic stress", contribution=0.15, direction="positive"),
        RiskFactor(factor="Military buildup", contribution=0.05, direction="positive")
    ]
    
    return {"country": country_code, "factors": factors}


@router.get("/{country_code}/history")
async def get_conflict_history(country_code: str):
    if country_code not in COUNTRY_NAMES:
        raise HTTPException(status_code=404, detail="Country not found")
    
    conflicts = [
        {"year": 2020, "type": "border_skirmish", "opponent": random.choice(list(COUNTRY_NAMES.keys()))},
        {"year": 2015, "type": "interstate", "opponent": random.choice(list(COUNTRY_NAMES.keys()))},
        {"year": 2010, "type": "civil_war", "opponent": "Internal"}
    ]
    
    return {"country": country_code, "conflicts": conflicts}