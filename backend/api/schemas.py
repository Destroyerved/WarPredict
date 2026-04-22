from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ConflictType(str, Enum):
    CIVIL_WAR = "civil_war"
    INTERSTATE = "interstate"
    PROXY = "proxy"
    TERRORISM = "terrorism"
    BORDER_SKIRMISH = "border_skirmish"


class RegimeType(str, Enum):
    DEMOCRACY = "democracy"
    AUTOCRACY = "autocracy"
    ANOCRACY = "anocracy"


class CountryFeatures(BaseModel):
    country_code: str
    year: int
    gdp_per_capita: float
    gdp_growth_rate: float
    military_expenditure_pct_gdp: float
    armed_forces_size: int
    political_instability_index: float
    human_development_index: float
    ethnic_fractionalization: float
    polity_score: int
    regime_type: RegimeType
    nuclear_capable: bool
    years_since_last_conflict: int
    past_conflict_count_10yr: int
    global_peace_index: float


class DyadFeatures(BaseModel):
    country_a: str
    country_b: str
    trade_dependency: float
    contiguous_border: bool
    shared_alliance: bool
    distance_km: float
    rivalry_score: float
    diplomatic_tensions: float
    news_sentiment_30d: float
    hostile_event_count_30d: int
    diplomatic_crisis_flag: bool


class PredictionRequest(BaseModel):
    dyad_features: DyadFeatures
    years_ahead: int = Field(default=1, ge=1, le=10)


class PredictionResponse(BaseModel):
    conflict_probability: float
    risk_level: str
    confidence_interval: tuple[float, float]
    key_factors: List[str]


class ConflictTypeRequest(BaseModel):
    country_features: CountryFeatures
    external_actor_involvement: float


class ConflictTypeResponse(BaseModel):
    conflict_type: ConflictType
    confidence: float
    probabilities: Dict[str, float]


class OutcomeRequest(BaseModel):
    country_a: str
    country_b: str
    military_a: float
    military_b: float
    economy_a: float
    economy_b: float
    nuclear_enabled: bool = False


class OutcomeResponse(BaseModel):
    duration_days: int
    estimated_casualties: int
    economic_damage_usd: int
    duration_ci: List[int]
    casualties_ci: List[int]
    economic_ci: List[int]
    winner_probability: Dict[str, float]


class SimulationScenario(BaseModel):
    country_a: str
    country_b: str
    military_a: float = Field(default=50, ge=0, le=100)
    military_b: float = Field(default=50, ge=0, le=100)
    economy_a: float = Field(default=50, ge=0, le=100)
    economy_b: float = Field(default=50, ge=0, le=100)
    resolve_a: float = Field(default=50, ge=0, le=100)
    resolve_b: float = Field(default=50, ge=0, le=100)
    alliances_a: List[str] = []
    alliances_b: List[str] = []
    nuclear_enabled: bool = False
    sanctions: List[str] = []


class SimulationResponse(BaseModel):
    scenario: Dict[str, Any]
    simulation_results: Dict[str, Any]
    alliance_cascade: Dict[str, Any]
    nuclear_deterrence: Optional[Dict[str, Any]]


class CountryProfile(BaseModel):
    code: str
    name: str
    gdp: float
    population: int
    military_expenditure: float
    stability_score: float
    nuclear_capable: bool
    recent_conflicts: int
    risk_score: float


class RiskFactor(BaseModel):
    factor: str
    contribution: float
    direction: str