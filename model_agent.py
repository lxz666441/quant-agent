"""Model Agent - Trains model and generates predictions."""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from loguru import logger
from config import MODEL_TYPE, TRAIN_WINDOW


class ModelAgent:
    """Agent responsible for model training and prediction."""
    
    def __init__(self):
        self.models = {}
        self.is_trained = False
        
    def predict(self, features):
        """Generate predictions and ranking."""
        logger.info("Starting model inference...")
        
        if not self.is_trained:
            self._train(features)
        
        # Generate predictions
        predictions = self._ensemble_predict(features)
        
        # Rank by limit-up probability
        ranked = self._rank_predictions(predictions)
        
        logger.info(f"Model inference complete: top stock probability {ranked.iloc[0]['probability']:.2%}")
        return ranked
    
    def _train(self, features):
        """Train ensemble model."""
        logger.info("Training ensemble model...")
        
        # Prepare training data
        X = features.drop(["target", "stock_code"], axis=1, errors="ignore")
        y = features.get("target", pd.Series([0] * len(features)))
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Train models
        self.models["rf"] = RandomForestClassifier(n_estimators=100)
        self.models["gb"] = GradientBoostingClassifier(n_estimators=100)
        
        self.models["rf"].fit(X_train, y_train)
        self.models["gb"].fit(X_train, y_train)
        
        # Evaluate
        rf_score = self.models["rf"].score(X_test, y_test)
        gb_score = self.models["gb"].score(X_test, y_test)
        logger.info(f"Model trained - RF: {rf_score:.2%}, GB: {gb_score:.2%}")
        
        self.is_trained = True
    
    def _ensemble_predict(self, features):
        """Generate ensemble predictions."""
        X = features.drop(["target", "stock_code"], axis=1, errors="ignore")
        
        rf_pred = self.models["rf"].predict_proba(X)[:, 1]
        gb_pred = self.models["gb"].predict_proba(X)[:, 1]
        
        # Weighted ensemble
        ensemble_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        features["probability"] = ensemble_pred
        return features
    
    def _rank_predictions(self, predictions):
        """Rank stocks by limit-up probability."""
        ranked = predictions.sort_values("probability", ascending=False)
        ranked["rank"] = range(1, len(ranked) + 1)
        return ranked