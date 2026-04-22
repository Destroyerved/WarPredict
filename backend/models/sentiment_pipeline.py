import numpy as np
import pandas as pd
from typing import Dict, List
import re

class SentimentPipeline:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"
        self.sentiment_cache: Dict[str, float] = {}
    
    def analyze_text(self, text: str) -> float:
        keywords_positive = ["peace", "treaty", "cooperation", "agreement", "dialogue", "summit"]
        keywords_negative = ["war", "conflict", "attack", "military", "sanctions", "tension", "crisis", "invasion"]
        
        text_lower = text.lower()
        score = 0.0
        
        for kw in keywords_positive:
            if kw in text_lower:
                score += 0.15
        for kw in keywords_negative:
            if kw in text_lower:
                score -= 0.2
        
        return max(-1.0, min(1.0, score))
    
    def analyze_headlines(self, headlines: List[str]) -> Dict[str, float]:
        sentiments = []
        for headline in headlines:
            sentiments.append(self.analyze_text(headline))
        
        if not sentiments:
            return {"sentiment_score": 0.0, "hostile_events": 0, "positive_events": 0}
        
        avg_sentiment = np.mean(sentiments)
        hostile_count = sum(1 for s in sentiments if s < -0.2)
        positive_count = sum(1 for s in sentiments if s > 0.2)
        
        return {
            "sentiment_score": float(avg_sentiment),
            "hostile_events": hostile_count,
            "positive_events": positive_count,
            "overall_tension": float(np.std(sentiments)) if len(sentiments) > 1 else 0.0
        }
    
    def get_country_sentiment(self, country: str) -> float:
        if country in self.sentiment_cache:
            return self.sentiment_cache[country]
        
        sample_headlines = [
            f"{country} announces military exercises",
            f"{country} signs trade agreement",
            f"Diplomatic tensions rise involving {country}",
        ]
        
        result = self.analyze_headlines(sample_headlines)
        self.sentiment_cache[country] = result["sentiment_score"]
        return result["sentiment_score"]
    
    def get_dyad_sentiment(self, country_a: str, country_b: str) -> float:
        sentiment_a = self.get_country_sentiment(country_a)
        sentiment_b = self.get_country_sentiment(country_b)
        return (sentiment_a + sentiment_b) / 2