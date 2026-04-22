import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

class ConflictTypeClassifier:
    CONFLICT_TYPES = ["civil_war", "interstate", "proxy", "terrorism", "border_skirmish"]
    
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.CONFLICT_TYPES)
        self.feature_cols = [
            "polity_score", "regime_type", "ethnic_fractionalization",
            "political_instability_index", "external_actor_involvement",
            "years_since_last_conflict", "military_expenditure_pct_gdp"
        ]
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["regime_type"] = df["regime_type"].map({"democracy": 1, "anocracy": 0, "autocracy": -1})
        return df
    
    def train(self, X: pd.DataFrame, y: pd.Series):
        X = self.preprocess(X)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_val)
        report = classification_report(y_val, y_pred, target_names=self.CONFLICT_TYPES, output_dict=True)
        return report
    
    def predict(self, X: pd.DataFrame) -> dict:
        X = self.preprocess(X)
        probas = self.model.predict_proba(X)
        predictions = self.model.predict(X)
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "type": self.CONFLICT_TYPES[pred],
                "confidence": float(max(probas[i])),
                "probabilities": {t: float(p) for t, p in zip(self.CONFLICT_TYPES, probas[i])}
            })
        return results
    
    def get_feature_importance(self) -> pd.DataFrame:
        importance = self.model.feature_importances_
        return pd.DataFrame({
            "feature": self.feature_cols,
            "importance": importance
        }).sort_values("importance", ascending=False)