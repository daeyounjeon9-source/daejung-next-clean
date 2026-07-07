from services.exchanges.binance import BinanceExchange
from services.exchanges.bybit import BybitExchange
from services.exchanges.upbit import UpbitExchange
from services.exchanges.bithumb import BithumbExchange

class ExchangeFactory:
    EXCHANGES = {
        'Binance': BinanceExchange,
        'Bybit': BybitExchange,
        'Upbit': UpbitExchange,
        'Bithumb': BithumbExchange,
        'binance': BinanceExchange,
        'bybit': BybitExchange,
        'upbit': UpbitExchange,
        'bithumb': BithumbExchange,
    }

    @classmethod
    def create(cls, exchange_name, api_key='', secret_key=''):
        exchange_cls = cls.EXCHANGES.get(exchange_name or '')
        if not exchange_cls:
            raise ValueError('지원하지 않는 거래소입니다')
        return exchange_cls(api_key=api_key, secret_key=secret_key)

    @classmethod
    def names(cls):
        return ['Binance', 'Bybit', 'Upbit', 'Bithumb']
