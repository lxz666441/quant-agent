"""QuantAgent - Main orchestrator for multi-agent trading system."""
import asyncio
import schedule
import time
from datetime import datetime
from loguru import logger

from agents.data_collector import DataCollectorAgent
from agents.feature_engineer import FeatureEngineerAgent
from agents.model_agent import ModelAgent
from agents.risk_agent import RiskAgent
from agents.trade_agent import TradeAgent
from config import TRADING_HOUR, TRADING_MINUTE


class QuantAgentSystem:
    """Main orchestrator coordinating all agents."""
    
    def __init__(self):
        self.data_collector = DataCollectorAgent()
        self.feature_engineer = FeatureEngineerAgent()
        self.model_agent = ModelAgent()
        self.risk_agent = RiskAgent()
        self.trade_agent = TradeAgent()
        self.daily_token_usage = 0
        
    async def run_pipeline(self):
        """Execute full trading pipeline."""
        logger.info(f"Starting trading pipeline at {datetime.now()}")
        
        # Step 1: Data Collection
        raw_data = await self.data_collector.collect()
        logger.info(f"Collected {len(raw_data)} records")
        
        # Step 2: Feature Engineering
        features = self.feature_engineer.process(raw_data)
        logger.info(f"Engineered {features.shape[1]} features")
        
        # Step 3: Model Inference
        predictions = self.model_agent.predict(features)
        logger.info(f"Generated predictions for {len(predictions)} stocks")
        
        # Step 4: Risk Assessment
        risk_scores = self.risk_agent.assess(predictions)
        logger.info(f"Risk assessment completed")
        
        # Step 5: Trade Execution
        signals = self.trade_agent.generate_signals(risk_scores)
        logger.info(f"Generated {len(signals)} trading signals")
        
        # Update token usage
        self.daily_token_usage += self._estimate_tokens(raw_data, features, predictions)
        
        return signals
    
    def _estimate_tokens(self, raw_data, features, predictions):
        """Estimate token consumption."""
        return 2_000_000  # Daily budget
    
    def schedule_daily(self):
        """Schedule daily execution at 9:20 AM."""
        schedule.every().day.at(f"{TRADING_HOUR:02d}:{TRADING_MINUTE:02d}").do(
            lambda: asyncio.run(self.run_pipeline())
        )
        
    def run(self):
        """Run scheduler loop."""
        self.schedule_daily()
        logger.info("QuantAgent system started")
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__":
    system = QuantAgentSystem()
    system.run()