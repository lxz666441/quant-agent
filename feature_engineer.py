"""Feature Engineer Agent - Processes raw data into model-ready features."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from loguru import logger


class FeatureEngineerAgent:
    """Agent responsible for feature engineering and data standardization."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def process(self, raw_data):
        """Process raw data into features."""
        logger.info("Starting feature engineering...")
        
        df = raw_data.copy()
        
        # Technical indicators
        df = self._add_technical_indicators(df)
        
        # Standardization
        df = self._standardize(df)
        
        # Handle missing values
        df = df.fillna(0)
        
        logger.info(f"Feature engineering complete: {df.shape[1]} features")
        return df
    
    def _add_technical_indicators(self, df):
        """Add technical indicators."""
        # Moving averages
        df["ma5"] = df["close"].rolling(5).mean()
        df["ma10"] = df["close"].rolling(10).mean()
        df["ma20"] = df["close"].rolling(20).mean()
        
        # RSI
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = df["close"].ewm(span=12).mean()
        ema26 = df["close"].ewm(span=26).mean()
        df["macd"] = ema12 - ema26
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        
        # Volatility
        df["volatility"] = df["close"].rolling(20).std()
        
        return df
    
    def _standardize(self, df):
        """Standardize numeric features."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        return df