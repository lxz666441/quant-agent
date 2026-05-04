"""Configuration for QuantAgent system."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
OPENCLAW_API_KEY = os.getenv("OPENCLAW_API_KEY", "")

# Data Sources
DATA_SOURCES = {
    "a_share_realtime": "https://api.example.com/stock/realtime",
    "fund_flow": "https://api.example.com/stock/fundflow",
    "limit_up": "https://api.example.com/stock/limitup",
}

# Trading Parameters
TRADING_HOUR = 9
TRADING_MINUTE = 20
MAX_POSITIONS = 3
RISK_THRESHOLD = 0.7

# Model Parameters
MODEL_TYPE = "ensemble"
TRAIN_WINDOW = 60
PREDICT_HORIZON = 1

# Paths
DATA_DIR = "./data"
LOG_DIR = "./logs"
OUTPUT_DIR = "./output"

# Token Budget
DAILY_TOKEN_BUDGET = 2_000_000