import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Create realistic synthetic datasets for the WarPredict system
np.random.seed(42)

DATA_DIR = Path(__file__).parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Real country codes
COUNTRIES = {
    'USA', 'CHN', 'RUS', 'IND', 'PAK', 'IRN', 'ISR', 'TUR', 'DEU', 'GBR',
    'FRA', 'BRA', 'JPN', 'KOR', 'NGA', 'EGY', 'SAU', 'UKR', 'VEN', 'SYR',
    'IDN', 'MYS', 'THA', 'PHL', 'VNM', 'KHM', 'LAO', 'KEN', 'ETH', 'ZAF',
    'AGO', 'DZA', 'MAR', 'POL', 'AUS', 'CAN', 'MEX', 'CHL', 'ARG', 'GRC',
    'HUN', 'CZE', 'ROU', 'SVK', 'HRV', 'ALB', 'SRB', 'AZE', 'UZB', 'KAZ'
}

COUNTRY_LIST = sorted(list(COUNTRIES))

print("Generating realistic synthetic datasets...")

# 1. UCDP Armed Conflict Dataset
print("\n1. Generating UCDP Armed Conflict data...")
n_conflicts = 250
conflicts = []
for i in range(n_conflicts):
    start_year = np.random.randint(1980, 2024)
    duration = np.random.randint(1, 20)
    end_year = min(start_year + duration, 2024)
    
    country = np.random.choice(COUNTRY_LIST)
    is_internal = np.random.random() > 0.4
    if is_internal:
        other_actor = f"Rebel_{country}_{i}"
    else:
        other_actor = np.random.choice([c for c in COUNTRY_LIST if c != country])
    
    deaths = np.random.lognormal(5, 2) * 100
    intensity = np.random.choice([1, 2], p=[0.6, 0.4])
    
    conflicts.append({
        'year_start': start_year,
        'year_end': end_year,
        'conflict_id': 20000 + i,
        'conflict_name': f'Conflict_{i}',
        'dyad_id': 50000 + i,
        'side_a': country,
        'side_b': other_actor,
        'type_of_conflict': ['Extrasystemic', 'Interstate', 'Internal', 'Internationalized internal'][np.random.randint(0, 4)],
        'deaths_a': deaths * np.random.uniform(0.3, 0.8),
        'deaths_b': deaths * np.random.uniform(0.2, 0.7),
        'deaths_total': deaths,
        'deaths_civilians': deaths * np.random.uniform(0.1, 0.4),
        'intensity_level': intensity,
        'territory': np.random.choice([True, False], p=[0.7, 0.3]),
        'incompatibility': np.random.choice(['Territory', 'Government', 'Both'], p=[0.5, 0.3, 0.2])
    })

ucdp_df = pd.DataFrame(conflicts)
ucdp_df.to_csv(RAW_DIR / 'ucdp_armed_conflict.csv', index=False)
print(f"  Created {len(ucdp_df)} conflict records")

# 2. Dyadic Dataset (country pairs)
print("\n2. Generating Dyadic Relations data...")
dyads = []
for i, country_a in enumerate(COUNTRY_LIST[:30]):
    for country_b in COUNTRY_LIST[i+1:30]:
        dyad_id = 50000 + i * 100 + COUNTRY_LIST.index(country_b)
        
        # Some dyads have history
        past_conflicts = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])
        years_since = np.random.randint(1, 50) if past_conflicts > 0 else 999
        
        dyads.append({
            'dyad_id': dyad_id,
            'country_a': country_a,
            'country_b': country_b,
            'contiguity': np.random.choice([0, 1], p=[0.7, 0.3]),
            'colonial_history': np.random.choice([0, 1], p=[0.9, 0.1]),
            'shared_alliance': np.random.choice([0, 1], p=[0.8, 0.2]),
            'trade_flow': np.random.uniform(0, 10000),
            'distance_km': np.random.lognormal(8, 1.5),
            'rivalry': np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05]),
            'past_conflicts': past_conflicts,
            'years_since_last_conflict': years_since,
            'conflict_history': past_conflicts > 0,
            'major_power_dyad': np.random.choice([0, 1], p=[0.8, 0.2])
        })

dyadic_df = pd.DataFrame(dyads)
dyadic_df.to_csv(RAW_DIR / 'ucdp_dyadic.csv', index=False)
print(f"  Created {len(dyadic_df)} dyadic relations")

# 3. Non-state Conflict Dataset
print("\n3. Generating Non-State Conflict data...")
non_state = []
for i in range(150):
    start_year = np.random.randint(1980, 2024)
    duration = np.random.randint(1, 15)
    end_year = min(start_year + duration, 2024)
    
    country = np.random.choice(COUNTRY_LIST)
    group1 = f"Group_{i}_A"
    group2 = f"Group_{i}_B"
    
    deaths = np.random.lognormal(4, 2) * 50
    
    non_state.append({
        'year_start': start_year,
        'year_end': end_year,
        'conflict_id': 30000 + i,
        'conflict_name': f'Non_state_{i}',
        'location': country,
        'side_a': group1,
        'side_b': group2,
        'type': np.random.choice(['Communal', 'Social', 'Factional']),
        'deaths_total': deaths,
        'deaths_civilians': deaths * np.random.uniform(0.3, 0.8),
        'intensity': np.random.choice([1, 2]),
        'issue': np.random.choice(['Resources', 'Power', 'Identity'], p=[0.4, 0.4, 0.2])
    })

non_state_df = pd.DataFrame(non_state)
non_state_df.to_csv(RAW_DIR / 'ucdp_non_state.csv', index=False)
print(f"  Created {len(non_state_df)} non-state conflicts")

# 4. Country Profile Dataset (for current country stats)
print("\n4. Generating Country Profile data...")
country_profiles = []
for country in COUNTRY_LIST:
    country_profiles.append({
        'country_code': country,
        'country_name': country,
        'gdp_current_usd': np.random.lognormal(20, 2),
        'gdp_per_capita': np.random.uniform(500, 60000),
        'gdp_growth_rate': np.random.normal(3, 3),
        'military_expenditure_usd': np.random.lognormal(18, 2),
        'military_expenditure_pct_gdp': np.random.uniform(0.5, 5),
        'armed_forces_size': np.random.lognormal(11, 2),
        'population_total': np.random.lognormal(17, 2),
        'population_growth': np.random.normal(2, 2),
        'political_instability_index': np.random.uniform(-4, 2),
        'human_development_index': np.random.uniform(0.4, 0.95),
        'ethnic_fractionalization': np.random.uniform(0, 0.9),
        'polity_score': np.random.randint(-10, 10),
        'regime_type': np.random.choice(['Democracy', 'Autocracy', 'Anocracy']),
        'nuclear_capable': np.random.choice([0, 1], p=[0.95, 0.05]),
        'global_peace_index': np.random.uniform(1, 3.5),
        'corruption_perceptions_index': np.random.uniform(20, 90),
        'year': 2024
    })

profiles_df = pd.DataFrame(country_profiles)
profiles_df.to_csv(PROCESSED_DIR / 'country_profiles_2024.csv', index=False)
print(f"  Created {len(profiles_df)} country profiles")

# 5. Dyadic Features Dataset (for prediction)
print("\n5. Generating Dyadic Features data...")
dyadic_features = []
for i, (ca, cb) in enumerate(zip(COUNTRY_LIST[:25], COUNTRY_LIST[1:26])):
    conflict_occurred = np.random.choice([0, 1], p=[0.85, 0.15])
    
    dyadic_features.append({
        'dyad_id': 60000 + i,
        'country_a': ca,
        'country_b': cb,
        'year': 2023,
        'gdp_per_capita_a': np.random.uniform(500, 60000),
        'gdp_per_capita_b': np.random.uniform(500, 60000),
        'gdp_growth_rate_a': np.random.normal(3, 3),
        'gdp_growth_rate_b': np.random.normal(3, 3),
        'military_expenditure_pct_gdp_a': np.random.uniform(0.5, 5),
        'military_expenditure_pct_gdp_b': np.random.uniform(0.5, 5),
        'armed_forces_size_a': np.random.lognormal(11, 2),
        'armed_forces_size_b': np.random.lognormal(11, 2),
        'political_instability_index_a': np.random.uniform(-4, 2),
        'political_instability_index_b': np.random.uniform(-4, 2),
        'human_development_index_a': np.random.uniform(0.4, 0.95),
        'human_development_index_b': np.random.uniform(0.4, 0.95),
        'ethnic_fractionalization_a': np.random.uniform(0, 0.9),
        'ethnic_fractionalization_b': np.random.uniform(0, 0.9),
        'polity_score_a': np.random.randint(-10, 10),
        'polity_score_b': np.random.randint(-10, 10),
        'nuclear_capable_a': np.random.choice([0, 1], p=[0.95, 0.05]),
        'nuclear_capable_b': np.random.choice([0, 1], p=[0.95, 0.05]),
        'years_since_last_conflict_a': np.random.randint(1, 50),
        'years_since_last_conflict_b': np.random.randint(1, 50),
        'past_conflict_count_10yr_a': np.random.randint(0, 5),
        'past_conflict_count_10yr_b': np.random.randint(0, 5),
        'global_peace_index_a': np.random.uniform(1, 3.5),
        'global_peace_index_b': np.random.uniform(1, 3.5),
        'trade_dependency': np.random.uniform(0, 0.5),
        'contiguous_border': np.random.choice([0, 1], p=[0.7, 0.3]),
        'shared_alliance': np.random.choice([0, 1], p=[0.8, 0.2]),
        'distance_km': np.random.lognormal(8, 1.5),
        'rivalry_score': np.random.uniform(0, 1),
        'diplomatic_tensions': np.random.uniform(0, 1),
        'news_sentiment_30d': np.random.normal(0, 0.3),
        'hostile_event_count_30d': np.random.poisson(2),
        'diplomatic_crisis_flag': np.random.choice([0, 1], p=[0.9, 0.1]),
        'conflict_occurred': conflict_occurred
    })

dyadic_features_df = pd.DataFrame(dyadic_features)
dyadic_features_df.to_csv(PROCESSED_DIR / 'dyadic_features.csv', index=False)
print(f"  Created {len(dyadic_features_df)} dyadic features records")

print("\nAll datasets generated successfully!")
print(f"  Raw data: {RAW_DIR}")
print(f"  Processed data: {PROCESSED_DIR}")
