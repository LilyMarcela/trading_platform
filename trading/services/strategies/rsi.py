# trading/services/strategies/rsi.py

import pandas as pd
import numpy as np
from .base import BaseStrategy

class RSIStrategy(BaseStrategy):
    """RSI-based Trading Strategy"""

    def __init__(self, strategy_config):
        super().__init__(strategy_config)
        self.overbought = strategy_config.get('overbought', 70)
        self.oversold = strategy_config.get('oversold', 30)

    def generate_signals(self, market_data):
        """Generates buy/sell signals based on RSI levels"""
        signals = pd.DataFrame(index=market_data.index)
        signals['signal'] = 0.0

        delta = market_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # Generate signals
        signals['signal'] = np.where(rsi > self.overbought, -1.0, np.where(rsi < self.oversold, 1.0, 0.0))

        return signals
