from services.exchange_base import ExchangeBase
class BithumbExchange(ExchangeBase):
    name = 'Bithumb'
    def get_balance(self):
        return {'KRW': 900000, 'BTC': 0.0065} if self.connected else {}
