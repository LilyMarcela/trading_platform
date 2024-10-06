# Pre-built strategy templates with default parameters
PRE_BUILT_STRATEGIES = {
    'macd': {
        'name': 'MACD Strategy',
        'description': 'Moving Average Convergence Divergence strategy',
        'default_parameters': {
            'macd_fast_period': 12,
            'macd_slow_period': 26,
            'macd_signal_period': 9,
        }
    },
    'rsi': {
        'name': 'RSI Strategy',
        'description': 'Relative Strength Index strategy',
        'default_parameters': {
            'rsi_period': 14,
            'rsi_overbought_level': 70,
            'rsi_oversold_level': 30,
        }
    },
    # Add more pre-built strategies as needed
}
