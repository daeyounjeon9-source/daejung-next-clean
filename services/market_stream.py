import random

class MarketStream:
    def __init__(self):
        self.last_price = 65000.0

    def next_price(self, symbol='BTCUSDT'):
        move = random.uniform(-350, 350)
        self.last_price = max(1, self.last_price + move)
        return round(self.last_price, 2)

market_stream = MarketStream()
