PLUGIN_TYPE = "strategy"
PLUGIN_NAME = "EMA RSI Sample"
PLUGIN_VERSION = "1.0.0"


def get_strategy():
    return {
        "name": "EMA_RSI_SAMPLE",
        "description": "EMA20 > EMA60 and RSI14 < 35 sample strategy.",
        "entry": ["EMA20 > EMA60", "RSI14 < 35"],
        "exit": ["TP 5%", "SL 2%"],
        "risk": {
            "take_profit": 5.0,
            "stop_loss": 2.0,
            "leverage": 3,
        },
    }


def check_signal(market_data: dict) -> str:
    ema20 = float(market_data.get("ema20", 0))
    ema60 = float(market_data.get("ema60", 0))
    rsi14 = float(market_data.get("rsi14", 50))
    if ema20 > ema60 and rsi14 < 35:
        return "BUY"
    return "WAIT"
