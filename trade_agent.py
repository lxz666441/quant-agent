"""Trade Agent - Generates trading signals and alerts."""
import pandas as pd
from datetime import datetime
from loguru import logger
from config import MAX_POSITIONS


class TradeAgent:
    """Agent responsible for trade signal generation."""
    
    def __init__(self):
        self.max_positions = MAX_POSITIONS
        
    def generate_signals(self, risk_assessed_data):
        """Generate trading signals from risk-assessed predictions."""
        logger.info("Generating trading signals...")
        
        df = risk_assessed_data.copy()
        
        # Filter passing risk assessment
        qualified = df[df["pass_risk"] == True].copy()
        
        # Sort by probability
        qualified = qualified.sort_values("probability", ascending=False)
        
        # Select top N positions
        signals = qualified.head(self.max_positions).copy()
        
        # Add signal metadata
        signals["signal_time"] = datetime.now()
        signals["action"] = "BUY"
        signals["confidence"] = signals["probability"].apply(self._confidence_level)
        
        # Generate alert message
        alert = self._generate_alert(signals)
        logger.info(f"Trading signals generated: {len(signals)} stocks")
        logger.info(f"Alert: {alert}")
        
        return signals
    
    def _confidence_level(self, prob):
        """Convert probability to confidence level."""
        if prob >= 0.8:
            return "HIGH"
        elif prob >= 0.6:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_alert(self, signals):
        """Generate alert message."""
        if signals.empty:
            return "No trading signals today."
        
        lines = ["=== Daily Trading Signals ==="]
        for _, row in signals.iterrows():
            lines.append(
                f"{row['stock_code']}: {row['action']} "
                f"(Prob: {row['probability']:.1%}, "
                f"Confidence: {row['confidence']})"
            )
        return "\n".join(lines)