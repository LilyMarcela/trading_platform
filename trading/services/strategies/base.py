# trading/services/strategies/base.py

from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """Abstract base class for all trading strategies"""

    def __init__(self, strategy_config):
        self.strategy_config = strategy_config

    @abstractmethod
    def generate_signals(self, market_data):
        """Method that must be implemented by all strategies to generate buy/sell signals"""
        pass
