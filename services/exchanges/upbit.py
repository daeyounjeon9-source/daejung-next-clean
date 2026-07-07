from services.exchange_base import ExchangeBase
class UpbitExchange(ExchangeBase):
    name = 'Upbit'
    def get_balance(self):
        return {'KRW': 1500000, 'BTC': 0.0080} if self.connected else {}
