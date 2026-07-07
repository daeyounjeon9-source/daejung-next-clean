from services.exchange_base import ExchangeBase
class BybitExchange(ExchangeBase):
    name = 'Bybit'
    def get_balance(self):
        return {'USDT': 800.00, 'BTC': 0.0100} if self.connected else {}
