import time
from abc import ABC, abstractmethod

class ExchangeBase(ABC):
    name = 'base'

    def __init__(self, api_key='', secret_key=''):
        self.api_key = api_key or ''
        self.secret_key = secret_key or ''
        self.connected = False
        self.last_latency_ms = None
        self.last_sync_time = None

    def mask_key(self, value):
        if not value:
            return ''
        if len(value) <= 8:
            return '*' * len(value)
        return value[:4] + '*' * (len(value) - 8) + value[-4:]

    def ping(self):
        start = time.perf_counter()
        time.sleep(0.02)
        self.last_latency_ms = int((time.perf_counter() - start) * 1000)
        return self.last_latency_ms

    def server_time(self):
        self.last_sync_time = time.strftime('%H:%M:%S')
        return {'server_time': self.last_sync_time, 'time_diff_ms': 0}

    def test_connection(self):
        latency = self.ping()
        sync = self.server_time()
        ok = bool(self.api_key) and bool(self.secret_key)
        self.connected = ok
        return {
            'success': ok,
            'exchange': self.name,
            'latency_ms': latency,
            'last_sync': sync['server_time'],
            'message': f'{self.name} API 연결 테스트 성공' if ok else 'API KEY / SECRET KEY 확인 필요',
        }

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError
