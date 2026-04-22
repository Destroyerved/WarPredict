import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

def ensure_dirs():
    """Create data directories if they don't exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def load_ucdp_conflicts() -> pd.DataFrame:
    """Load UCDP armed conflict data."""
    ensure_dirs()
    filepath = RAW_DIR / "ucdp_armed_conflict.csv"
    
    if filepath.exists() and filepath.stat().st_size > 100:
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} conflict records from UCDP")
            return df
        except Exception as e:
            logger.warning(f"Error loading UCDP data: {e}")
    
    logger.warning("UCDP conflict data not found, generating synthetic data")
    return generate_synthetic_conflicts()

def load_dyadic_relations() -> pd.DataFrame:
    """Load dyadic relations data."""
    ensure_dirs()
    filepath = RAW_DIR / "ucdp_dyadic.csv"
    
    if filepath.exists() and filepath.stat().st_size > 100:
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} dyadic relations")
            return df
        except Exception as e:
            logger.warning(f"Error loading dyadic data: {e}")
    
    logger.warning("Dyadic relations data not found, generating synthetic data")
    return generate_synthetic_dyadic_relations()

def load_non_state_conflicts() -> pd.DataFrame:
    """Load non-state conflict data."""
    ensure_dirs()
    filepath = RAW_DIR / "ucdp_non_state.csv"
    
    if filepath.exists() and filepath.stat().st_size > 100:
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} non-state conflicts")
            return df
        except Exception as e:
            logger.warning(f"Error loading non-state data: {e}")
    
    logger.warning("Non-state conflict data not found")
    return pd.DataFrame()

def load_country_profiles() -> pd.DataFrame:
    """Load country profile data."""
    ensure_dirs()
    filepath = PROCESSED_DIR / "country_profiles_2024.csv"
    
    if filepath.exists() and filepath.stat().st_size > 100:
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded profiles for {len(df)} countries")
            return df
        except Exception as e:
            logger.warning(f"Error loading country profiles: {e}")
    
    logger.warning("Country profiles not found, generating synthetic data")
    return generate_synthetic_country_profiles()

def load_dyadic_features() -> pd.DataFrame:
    """Load dyadic features for prediction."""
    ensure_dirs()
    filepath = PROCESSED_DIR / "dyadic_features.csv"
    
    if filepath.exists() and filepath.stat().st_size > 100:
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} dyadic feature records")
            return df
        except Exception as e:
            logger.warning(f"Error loading dyadic features: {e}")
    
    logger.warning("Dyadic features not found, generating synthetic data")
    return generate_synthetic_dyadic_features()

def get_available_countries() -> List[str]:
    """Get list of available countries from profiles."""
    default_countries = [
        "USA", "CHN", "RUS", "IND", "PAK", "IRN", "ISR", "TUR",
        "DEU", "GBR", "FRA", "BRA", "JPN", "KOR", "NGA", "EGY",
        "SAU", "UKR", "VEN", "SYR", "PRK", "AUS", "CAN", "MEX"
    ]
    
    profiles = load_country_profiles()
    if not profiles.empty and 'country_code' in profiles.columns:
        return profiles['country_code'].unique().tolist()
    
    return default_countries

def generate_synthetic_country_profiles() -> pd.DataFrame:
    """Generate synthetic country profile data if real data is unavailable."""
    countries = [
        "USA", "CHN", "RUS", "IND", "PAK", "IRN", "ISR", "TUR",
        "DEU", "GBR", "FRA", "BRA", "JPN", "KOR", "NGA", "EGY",
        "SAU", "UKR", "VEN", "SYR", "PRK", "AUS", "CAN", "MEX"
    ]
    profiles = []
    
    for country in countries:
        profile = {
            'country_code': country,
            'country_name': country,
            'gdp_per_capita': np.random.uniform(1000, 80000),
            'gdp_growth_rate': np.random.uniform(-5, 10),
            'military_expenditure_pct_gdp': np.random.uniform(1, 6),
            'armed_forces_size': int(np.random.uniform(50000, 2000000)),
            'political_instability_index': np.random.uniform(20, 90),
            'human_development_index': np.random.uniform(0.4, 0.95),
            'ethnic_fractionalization': np.random.uniform(0.1, 0.8),
            'polity_score': np.random.randint(-10, 10),
            'regime_type': np.random.choice(["democracy", "autocracy", "anocracy"]),
            'nuclear_capable': country in ["USA", "RUS", "CHN", "IND", "PAK", "FRA", "GBR"],
            'years_since_last_conflict': int(np.random.randint(0, 30)),
            'past_conflict_count_10yr': int(np.random.randint(0, 5)),
            'global_peace_index': np.random.uniform(1.5, 3.5),
        }
        profiles.append(profile)
    
    return pd.DataFrame(profiles)

def generate_synthetic_dyadic_features(num_dyads: int = 100) -> pd.DataFrame:
    """Generate synthetic dyadic features for training."""
    countries = get_available_countries()
    dyads = []
    
    for _ in range(num_dyads):
        if len(countries) < 2:
            break
        country_a, country_b = np.random.choice(countries, 2, replace=False)
        dyad = {
            'dyad_id': f"{country_a}_{country_b}",
            'country_a': country_a,
            'country_b': country_b,
            'trade_dependency': np.random.uniform(0.01, 0.3),
            'contiguous_border': np.random.choice([True, False], p=[0.3, 0.7]),
            'shared_alliance': np.random.choice([True, False], p=[0.2, 0.8]),
            'distance_km': np.random.uniform(100, 15000),
            'rivalry_score': np.random.uniform(0, 1),
            'diplomatic_tensions': np.random.uniform(0, 1),
            'news_sentiment_30d': np.random.uniform(-0.5, 0.5),
            'hostile_event_count_30d': int(np.random.randint(0, 20)),
            'diplomatic_crisis_flag': np.random.choice([True, False], p=[0.1, 0.9]),
            'conflict_onset_5yr': np.random.choice([0, 1], p=[0.85, 0.15])
        }
        dyads.append(dyad)
    
    return pd.DataFrame(dyads)

def generate_synthetic_conflicts() -> pd.DataFrame:
    """Generate synthetic conflict data."""
    countries = get_available_countries()
    conflict_types = ["civil_war", "interstate", "proxy", "terrorism", "border_skirmish"]
    conflicts = []
    
    for i in range(50):
        if len(countries) < 2:
            break
        side_a, side_b = np.random.choice(countries, 2, replace=False)
        conflict = {
            'conflict_id': f"conf_{i}",
            'year_start': np.random.randint(2000, 2024),
            'side_a': side_a,
            'side_b': side_b,
            'type': np.random.choice(conflict_types),
            'deaths': int(np.random.uniform(100, 100000)),
            'status': np.random.choice(['ongoing', 'terminated']),
        }
        conflicts.append(conflict)
    
    return pd.DataFrame(conflicts)

def generate_synthetic_dyadic_relations() -> pd.DataFrame:
    """Generate synthetic dyadic relations data."""
    countries = get_available_countries()
    relations = []
    
    for i in range(80):
        if len(countries) < 2:
            break
        country_a, country_b = np.random.choice(countries, 2, replace=False)
        relation = {
            'dyad_id': f"{country_a}_{country_b}_{i}",
            'country_a': country_a,
            'country_b': country_b,
            'relation_type': np.random.choice(['allied', 'neutral', 'rival']),
            'trade_volume': np.random.uniform(1e6, 1e10),
            'joint_memberships': int(np.random.randint(0, 5)),
        }
        relations.append(relation)
    
    return pd.DataFrame(relations)

def get_country_info(country_code: str) -> Optional[Dict]:
    """Get info for a specific country."""
    profiles = load_country_profiles()
    if not profiles.empty:
        country_data = profiles[profiles['country_code'] == country_code]
        if not country_data.empty:
            return country_data.iloc[0].to_dict()
    return None

def get_all_conflicts() -> pd.DataFrame:
    """Get all conflicts (both interstate and non-state)."""
    interstate = load_ucdp_conflicts()
    non_state = load_non_state_conflicts()
    
    if not interstate.empty and not non_state.empty:
        return pd.concat([interstate, non_state], ignore_index=True)
    elif not interstate.empty:
        return interstate
    elif not non_state.empty:
        return non_state
    else:
        return pd.DataFrame()

def get_country_conflicts(country_code: str) -> pd.DataFrame:
    """Get all conflicts involving a specific country."""
    conflicts = get_all_conflicts()
    if conflicts.empty:
        return pd.DataFrame()
    
    mask = (
        conflicts.get('side_a', '').astype(str).str.contains(country_code, na=False) |
        conflicts.get('side_b', '').astype(str).str.contains(country_code, na=False) |
        conflicts.get('location', '').astype(str).str.contains(country_code, na=False)
    )
    return conflicts[mask]

def get_conflict_statistics() -> Dict:
    """Get overall conflict statistics."""
    conflicts = get_all_conflicts()
    if not conflicts.empty:
        return {
            'total_conflicts': len(conflicts),
            'total_deaths': conflicts.get('deaths', pd.Series([0])).sum(),
            'avg_duration_years': 5,
            'conflicts_by_type': conflicts.get('type', pd.Series()).value_counts().to_dict()
        }
    return {'total_conflicts': 0, 'total_deaths': 0, 'avg_duration_years': 0}

# Cache data in memory
_cache = {}

def get_cache(key: str, loader_func, *args, **kwargs):
    """Get cached data or load it."""
    if key not in _cache:
        _cache[key] = loader_func(*args, **kwargs)
    return _cache[key]

def clear_cache():
    """Clear data cache."""
    global _cache
    _cache = {}
    df.to_parquet(output_file, index=False)
    print(f"  Generated sample SIPRI data: {len(df)} rows")
    return df

def download_fragile_states() -> pd.DataFrame:
    ensure_dirs()
    
    print("  Note: FSI requires manual download - using sample data")
    countries = get_country_list()
    years = list(range(2018, 2025))
    
    data = []
    for country in countries:
        for year in years:
            np.random.seed(hash(country + str(year)) % 2**32)
            score = np.random.uniform(20, 110)
            data.append({
                'country_code': country,
                'year': year,
                'fsi_score': score,
                'rank': int(score)
            })
    
    df = pd.DataFrame(data)
    output_file = PROCESSED_DIR / "fragile_states.parquet"
    df.to_parquet(output_file, index=False)
    print(f"  Generated sample FSI data: {len(df)} rows")
    return df

def download_global_peace_index() -> pd.DataFrame:
    ensure_dirs()
    
    print("  Note: GPI requires manual download - using sample data")
    countries = get_country_list()
    years = list(range(2018, 2025))
    
    data = []
    for country in countries:
        for year in years:
            np.random.seed(hash(country + str(year)) % 2**32)
            score = np.random.uniform(1.5, 3.5)
            data.append({
                'country_code': country,
                'year': year,
                'gpi_score': score,
                'peace_rank': int(score * 50)
            })
    
    df = pd.DataFrame(data)
    output_file = PROCESSED_DIR / "global_peace_index.parquet"
    df.to_parquet(output_file, index=False)
    print(f"  Generated sample GPI data: {len(df)} rows")
    return df

def download_polity_data() -> pd.DataFrame:
    ensure_dirs()
    
    print("  Note: Polity V requires manual download - using sample data")
    countries = get_country_list()
    years = list(range(2018, 2024))
    
    data = []
    for country in countries:
        for year in years:
            np.random.seed(hash(country + str(year)) % 2**32)
            polity = np.random.randint(-10, 11)
            data.append({
                'country_code': country,
                'year': year,
                'polity_score': polity,
                'polity2': polity,
                'x_corruption': np.random.randint(1, 7),
                'xr_reg': np.random.randint(0, 7),
                'xc_reg': np.random.randint(0, 7)
            })
    
    df = pd.DataFrame(data)
    output_file = PROCESSED_DIR / "polity5.parquet"
    df.to_parquet(output_file, index=False)
    print(f"  Generated sample Polity data: {len(df)} rows")
    return df

def load_processed_data() -> dict:
    data = {}
    for f in PROCESSED_DIR.glob("*.parquet"):
        name = f.stem
        try:
            data[name] = pd.read_parquet(f)
            print(f"Loaded {name}: {len(data[name])} rows")
        except Exception as e:
            print(f"Error loading {f}: {e}")
    return data

def download_all_data():
    print("\n=== Downloading Datasets ===\n")
    
    print("[1/7] World Bank Data...")
    download_world_bank_data()
    
    print("\n[2/7] UCDP Conflict Data...")
    download_ucdp_data()
    
    print("\n[3/7] Fragile States Index...")
    download_fragile_states()
    
    print("\n[4/7] Global Peace Index...")
    download_global_peace_index()
    
    print("\n[5/7] Polity V Data...")
    download_polity_data()
    
    print("\n[6/7] SIPRI Military Expenditure...")
    download_sipri_milex()
    
    print("\n[7/7] Loading processed data...")
    data = load_processed_data()
    
    print(f"\n=== Download Complete ===")
    print(f"Loaded {len(data)} datasets")
    return data

def get_country_list() -> list:
    return [
        "USA", "CHN", "RUS", "IND", "PAK", "IRN", "ISR", "TUR", "DEU", "GBR",
        "FRA", "BRA", "JPN", "KOR", "NGA", "EGY", "SAU", "UKR", "VEN", "SYR",
        "IRQ", "AFG", "YEM", "LBY", "SSD", "SOM", "NER", "MLI", "TCD", "COG"
    ]

if __name__ == "__main__":
    download_all_data()