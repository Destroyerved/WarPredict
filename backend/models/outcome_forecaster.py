import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

class OutcomeForecaster:
    def __init__(self):
        self.duration_model = xgb.XGBRegressor(
            n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
        )
        self.casualties_model = xgb.XGBRegressor(
            n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
        )
        self.economic_model = xgb.XGBRegressor(
            n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
        )
        self.feature_cols = [
            "military_expenditure_pct_gdp", "armed_forces_size",
            "political_instability_index", "rivalry_score",
            "distance_km", "contiguous_border", "nuclear_capable"
        ]
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["nuclear_capable"] = df["nuclear_capable"].astype(int)
        df["contiguous_border"] = df["contiguous_border"].astype(int)
        return df
    
    def train(self, X: pd.DataFrame, y_duration: pd.Series, y_casualties: pd.Series, y_economic: pd.Series):
        X = self.preprocess(X)
        X_train, X_val, y_dur_train, y_dur_val = train_test_split(X, y_duration, test_size=0.2, random_state=42)
        _, _, y_cas_train, y_cas_val = train_test_split(X, y_casualties, test_size=0.2, random_state=42)
        _, _, y_eco_train, y_eco_val = train_test_split(X, y_economic, test_size=0.2, random_state=42)
        
        self.duration_model.fit(X_train, y_dur_train)
        self.casualties_model.fit(X_train, y_cas_train)
        self.economic_model.fit(X_train, y_eco_train)
        
        return {
            "duration_mae": mean_absolute_error(y_dur_val, self.duration_model.predict(X_val)),
            "casualties_mae": mean_absolute_error(y_cas_val, self.casualties_model.predict(X_val)),
            "economic_mae": mean_absolute_error(y_eco_val, self.economic_model.predict(X_val))
        }
    
    def predict(self, X: pd.DataFrame) -> dict:
        X = self.preprocess(X)
        duration = self.duration_model.predict(X)
        casualties = self.casualties_model.predict(X)
        economic = self.economic_model.predict(X)
        
        return {
            "duration_days": int(max(1, int(duration[0]))),
            "estimated_casualties": int(max(0, int(casualties[0]))),
            "economic_damage_usd": int(max(0, int(economic[0]))),
            "duration_ci": [int(duration[0] * 0.5), int(duration[0] * 1.5)],
            "casualties_ci": [int(casualties[0] * 0.3), int(casualties[0] * 1.7)],
            "economic_ci": [int(economic[0] * 0.4), int(economic[0] * 1.6)]
        }
    
    def get_feature_importance(self) -> pd.DataFrame:
        importance = self.duration_model.feature_importances_
        return pd.DataFrame({
            "feature": self.feature_cols,
            "importance": importance
        }).sort_values("importance", ascending=False)