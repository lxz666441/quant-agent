"""Risk Agent - Assesses risk for predicted stocks."""
import pandas as pd
import numpy as np
from loguru import logger
from config import RISK_THRESHOLD


class RiskAgent:
    """Agent responsible for risk assessment."""
    
    def __init__(self):
        self.risk_threshold = RISK_THRESHOLD
        
    def assess(self, predictions):
        """Assess risk for all predictions."""
        logger.info("Starting risk assessment...")
        
        df = predictions.copy()
        
        # Calculate risk scores
        df["volatility_risk"] = self._assess_volatility(df)
        df["liquidity_risk"] = self._assess_liquidity(df)
        df["sector_risk"] = self._assess_sector_heat(df)
        
        # Composite risk score
        df["risk_score"] = (
            0.4 * df["volatility_risk"] +
            0.3 * df["liquidity_risk"] +
            0.3 * df["sector_risk"]
        )
        
        # Filter by risk threshold
        df["pass_risk"] = df["risk_score"] < self.risk_threshold
        
        logger.info(f"Risk assessment complete: {df['pass_risk'].sum()} passed")
        return df
    
    def _assess_volatility(self, df):
        """Assess volatility risk."""
        volatility = df.get("volatility", pd.Series([0] * len(df)))
        # Normalize to 0-1
        return (volatility - volatility.min()) / (volatility.max() - volatility.min() + 1e-10)
    
    def _assess_liquidity(self, df):
        """Assess liquidity risk."""
        volume = df.get("volume", pd.Series([0] * len(df)))
        # Higher volume = lower risk
        liquidity = 1 - (volume - volume.min()) / (volume.max() - volume.min() + 1e-10)
        return liquidity
    
    def _assess_sector_heat(self, df):
        """Assess sector heat risk."""
        sector = df.get("sector", pd.Series(["unknown"] * len(df)))
        # Simplified: random sector heat
        np.random.seed(42)
        return pd.Series(np.random.random(len(df)), index=df.index)