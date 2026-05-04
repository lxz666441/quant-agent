# QuantAgent - AI-Driven Quantitative Trading System

An intelligent multi-agent quantitative trading decision system built with OpenClaw, featuring automated market data collection, feature engineering, model inference, risk assessment, and trade execution.

## Features

- **Multi-Agent Architecture**: 5 specialized agents working collaboratively
- **Automated Data Collection**: Daily market data scraping at 9:20 AM
- **Feature Engineering**: Technical indicators and data standardization
- **Model Inference**: Historical data training with limit-up probability ranking
- **Risk Assessment**: Volatility, liquidity, and sector heat analysis
- **Trade Execution**: Automated signal generation and alert推送

## Architecture

```
QuantAgent/
├── agents/
│   ├── data_collector.py    # Market data acquisition
│   ├── feature_engineer.py  # Feature engineering & standardization
│   ├── model_agent.py       # Prediction model & ranking
│   ├── risk_agent.py        # Risk assessment
│   └── trade_agent.py       # Signal generation & alerts
├── config.py                # Configuration
├── main.py                  # Orchestrator
└── requirements.txt         # Dependencies
```

## Performance

- Daily data processing: 5000+ records
- Token consumption: ~2M per day
- Backtest win rate: 68%
- Fully automated operation

## Tech Stack

- OpenClaw for agent orchestration
- Claude/GPT/DeepSeek/MiMo for reasoning
- Python 3.10+
- pandas, numpy, scikit-learn

## License

MIT