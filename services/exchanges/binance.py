from services.exchange_base import ExchangeBase
class BinanceExchange(ExchangeBase):
    name = 'Binance'
    def get_balance(self):
        return {'USDT': 1250.52, 'BTC': 0.0153, 'ETH': 0.20} if self.connected else {}
