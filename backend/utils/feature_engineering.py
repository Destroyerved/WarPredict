import pandas as pd
import numpy as np
from datetime import datetime

def create_country_features(year: int, country_code: str, world_bank_data: pd.DataFrame) -> dict:
    return {
        "country_code": country_code,
        "year": year,
        "gdp_per_capita": np.random.uniform(1000, 80000),
        "gdp_growth_rate": np.random.uniform(-5, 10),
        "military_expenditure_pct_gdp": np.random.uniform(1, 6),
        "armed_forces_size": int(np.random.uniform(50000, 2000000)),
        "political_instability_index": np.random.uniform(20, 90),
        "human_development_index": np.random.uniform(0.4, 0.95),
        "ethnic_fractionalization": np.random.uniform(0.1, 0.8),
        "polity_score": np.random.randint(-10, 10),
        "regime_type": np.random.choice(["democracy", "autocracy", "anocracy"]),
        "nuclear_capable": np.random.choice([True, False], p=[0.15, 0.85]),
        "years_since_last_conflict": int(np.random.randint(0, 30)),
        "past_conflict_count_10yr": int(np.random.randint(0, 5)),
        "global_peace_index": np.random.uniform(1.5, 3.5),
    }

def create_dyad_features(country_a: dict, country_b: dict) -> dict:
    return {
        "dyad_id": f"{country_a['country_code']}_{country_b['country_code']}",
        "country_a": country_a["country_code"],
        "country_b": country_b["country_code"],
        "trade_dependency": np.random.uniform(0.01, 0.3),
        "contiguous_border": np.random.choice([True, False], p=[0.3, 0.7]),
        "shared_alliance": np.random.choice([True, False], p=[0.2, 0.8]),
        "distance_km": np.random.uniform(100, 15000),
        "rivalry_score": np.random.uniform(0, 1),
        "diplomatic_tensions": np.random.uniform(0, 1),
    }

def create_conflict_target(conflict_history: list, year: int, years_ahead: int = 5) -> int:
    return np.random.choice([0, 1], p=[0.85, 0.15])

def engineer_features(countries: list, years: list) -> pd.DataFrame:
    country_features = []
    for year in years:
        for country in countries:
            country_features.append(create_country_features(year, country))
    return pd.DataFrame(country_features)

def add_nlp_sentiment(features: pd.DataFrame) -> pd.DataFrame:
    features["news_sentiment_30d"] = np.random.uniform(-0.5, 0.5, len(features))
    features["hostile_event_count_30d"] = np.random.randint(0, 20, len(features))
    features["diplomatic_crisis_flag"] = np.random.choice([True, False], p=[0.1, 0.9], size=len(features))
    return features