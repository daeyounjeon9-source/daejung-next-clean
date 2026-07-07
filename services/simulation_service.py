from datetime import datetime
import random

class SimulationService:
    """실제 주문 없이 전략 신호를 거래 결과처럼 검증."""
    def run_trade(self, config, market_data, decision, risk):
        entry = float(market_data.get('price', 65000))
        direction = decision.get('signal') or 'WAIT'
        if direction == 'WAIT' or not risk.get('allowed'):
            profit = 0.0
            exit_price = entry
            result = '대기'
        else:
            base = random.uniform(-1.2, 2.0)
            if decision.get('confidence', 0) > 65:
                base += 0.35
            profit = round(base, 2)
            if direction == 'SHORT':
                exit_price = entry * (1 - profit / 100)
            else:
                exit_price = entry * (1 + profit / 100)
            result = '성공' if profit >= 0 else '실패'
        return {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project_name': config.get('project_name', ''),
            'strategy': config.get('strategy', ''),
            'symbol': config.get('symbol', 'BTCUSDT'),
            'side': direction,
            'entry_price': round(entry, 2),
            'exit_price': round(exit_price, 2),
            'result': result,
            'profit_rate': profit,
            'memo': f"v02.8 전략엔진 모의실행 | {decision.get('reason','')} | {risk.get('message','')}"
        }
