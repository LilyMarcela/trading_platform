# trading/services/strategies/moving_average.py

import pandas as pd
import numpy as np
from .base import BaseStrategy

class MovingAverageCrossoverStrategy(BaseStrategy):
    """Moving Average Crossover Strategy"""

    def __init__(self, strategy_config):
        super().__init__(strategy_config)
        self.short_window = strategy_config.get('short_window', 50)
        self.long_window = strategy_config.get('long_window', 200)
    
    def generate_signals(self, market_data):
        """Generates buy/sell signals based on moving average crossovers"""
        signals = pd.DataFrame(index=market_data.index)
        signals['signal'] = 0.0
        
        # Create short and long moving averages
        signals['short_mavg'] = market_data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_mavg'] = market_data['Close'].rolling(window=self.long_window, min_periods=1).mean()

        # Buy signal when short MA crosses above long MA, sell when it crosses below
        signals['signal'][self.short_window:] = np.where(
            signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:], 1.0, 0.0)
        
        signals['positions'] = signals['signal'].diff()  # Capture changes (buy/sell signals)
        
        return signals
