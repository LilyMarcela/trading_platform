# trading/services/strategy_loader.py

from .strategies.moving_average import MovingAverageCrossoverStrategy
from .strategies.rsi import RSIStrategy

def load_strategy(strategy_name, strategy_config):
    """Dynamically loads the correct strategy class"""
    if strategy_name == 'Moving Average Crossover':
        return MovingAverageCrossoverStrategy(strategy_config)
    elif strategy_name == 'RSI':
        return RSIStrategy(strategy_config)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")
