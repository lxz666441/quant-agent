"""Data Collector Agent - Fetches market data from multiple sources."""
import asyncio
import requests
import pandas as pd
from loguru import logger
from config import DATA_SOURCES


class DataCollectorAgent:
    """Agent responsible for collecting real-time market data."""
    
    def __init__(self):
        self.sources = DATA_SOURCES
        
    async def collect(self):
        """Collect data from all configured sources."""
        logger.info("Starting data collection...")
        
        tasks = [
            self._fetch_realtime_quotes(),
            self._fetch_fund_flow(),
            self._fetch_limit_up_data(),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Merge all data sources
        combined_data = self._merge_data(results)
        logger.info(f"Data collection complete: {len(combined_data)} records")
        return combined_data
    
    async def _fetch_realtime_quotes(self):
        """Fetch real-time A-share quotes."""
        try:
            response = requests.get(self.sources["a_share_realtime"], timeout=30)
            data = response.json()
            return pd.DataFrame(data["stocks"])
        except Exception as e:
            logger.error(f"Failed to fetch realtime quotes: {e}")
            return pd.DataFrame()
    
    async def _fetch_fund_flow(self):
        """Fetch fund flow data."""
        try:
            response = requests.get(self.sources["fund_flow"], timeout=30)
            data = response.json()
            return pd.DataFrame(data["flows"])
        except Exception as e:
            logger.error(f"Failed to fetch fund flow: {e}")
            return pd.DataFrame()
    
    async def _fetch_limit_up_data(self):
        """Fetch limit-up stock data."""
        try:
            response = requests.get(self.sources["limit_up"], timeout=30)
            data = response.json()
            return pd.DataFrame(data["limit_ups"])
        except Exception as e:
            logger.error(f"Failed to fetch limit-up data: {e}")
            return pd.DataFrame()
    
    def _merge_data(self, results):
        """Merge data from multiple sources."""
        dfs = [r for r in results if isinstance(r, pd.DataFrame) and not r.empty]
        if not dfs:
            return pd.DataFrame()
        
        merged = dfs[0]
        for df in dfs[1:]:
            merged = merged.merge(df, on="stock_code", how="outer")
        
        return merged