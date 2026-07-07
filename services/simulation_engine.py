import random
from datetime import datetime
from core.position_manager import position_manager
from core.portfolio_manager import portfolio_manager
from services.market_stream import market_stream
from services.execution_service import execution_service

class SimulationEngine:
    def run_once(self, config):
        symbol = config.get('symbol', 'BTCUSDT') or 'BTCUSDT'
        side = random.choice(['LONG', 'SHORT'])
        entry_price = market_stream.next_price(symbol)
        try:
            amount = float(str(config.get('initial_amount', '1000000')).replace(',', ''))
        except Exception:
            amount = 1000000.0
        used_amount = amount * 0.1
        quantity = max(0.0001, used_amount / entry_price)
        order = execution_service.submit_simulation_order(symbol, side, quantity, entry_price)
        exit_price = market_stream.next_price(symbol)
        closed = position_manager.close_position(exit_price)
        profit_rate = float(closed.get('profit_rate', 0)) if closed else 0.0
        pnl = portfolio_manager.apply_result(profit_rate, used_amount)
        return {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project_name': config.get('project_name', ''),
            'exchange': config.get('exchange', ''),
            'strategy': config.get('strategy', ''),
            'symbol': symbol,
            'side': side,
            'entry_price': round(entry_price, 2),
            'exit_price': round(exit_price, 2),
            'quantity': round(quantity, 6),
            'profit_rate': round(profit_rate, 2),
            'pnl': round(pnl, 2),
            'result': '성공' if profit_rate >= 0 else '손실',
            'mode': 'SIMULATION',
            'order': getattr(order, 'order_id', ''),
            'portfolio': portfolio_manager.snapshot(),
        }

simulation_engine = SimulationEngine()
