from core.log_manager import add_log
from core.result_manager import save_result
from services.account_service import account_service
from services.simulation_engine import simulation_engine

class TradingEngine:
    def __init__(self):
        self.running = False
        self.mode = 'SIMULATION'
        self.last_result = None

    def validate(self, config):
        required = ['project_name', 'exchange', 'strategy', 'symbol', 'initial_amount']
        missing = [k for k in required if not str(config.get(k, '')).strip()]
        if missing:
            return False, '필수 설정 누락: ' + ', '.join(missing)
        if self.mode != 'SIMULATION':
            return False, '실거래는 아직 비활성화되어 있습니다.'
        return True, '거래 엔진 준비 완료(모의거래)'

    def start(self, config):
        ok, msg = self.validate(config)
        if not ok:
            add_log(msg, 'WARNING')
            return {'success': False, 'message': msg}
        account_service.load_from_config(config)
        self.running = True
        add_log('Trading Engine 시작 / SIMULATION', 'INFO')
        return {'success': True, 'message': '거래 엔진 모의 실행 시작'}

    def run_once(self, config):
        if not self.running:
            return None
        result = simulation_engine.run_once(config)
        path = save_result(result)
        result['saved_path'] = path
        self.last_result = result
        self.running = False
        add_log(f"거래 엔진 모의 실행 완료: {result.get('profit_rate')}%", 'SUCCESS')
        return result

    def stop(self):
        self.running = False
        add_log('Trading Engine 중지', 'WARNING')

trading_engine = TradingEngine()
