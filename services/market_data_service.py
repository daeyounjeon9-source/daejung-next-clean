from datetime import datetime
import random

class MarketDataService:
    """실거래 전 검증용 모의 시장 데이터 서비스."""
    def __init__(self):
        self.last_price = 65000.0

    def get_snapshot(self, symbol='BTCUSDT'):
        self.last_price = round(self.last_price * (1 + random.uniform(-0.003, 0.003)), 2)
        return {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol or 'BTCUSDT',
            'price': self.last_price,
            'volume': round(random.uniform(100, 900), 2),
            'trend': random.choice(['UP', 'DOWN', 'SIDE'])
        }

    def get_series(self, symbol='BTCUSDT', count=30):
        price = self.last_price
        rows = []
        for _ in range(count):
            price = round(price * (1 + random.uniform(-0.0025, 0.0025)), 2)
            rows.append({'symbol': symbol, 'price': price, 'volume': round(random.uniform(100, 900), 2)})
        self.last_price = price
        return rows
