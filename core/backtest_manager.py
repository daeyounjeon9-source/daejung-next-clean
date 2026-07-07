from __future__ import annotations

from services.backtest_service import BacktestConfig, run_backtest
from services.candle_loader import load_candles
from services.report_generator import save_backtest_result


class BacktestManager:
    def run(self, strategy="EMA Cross", symbol="BTCUSDT", initial_balance=10000000, fee_rate=0.05, candle_count=300):
        candles = load_candles(symbol=symbol, count=int(candle_count))
        config = BacktestConfig(
            strategy=strategy,
            symbol=symbol,
            initial_balance=float(initial_balance),
            fee_rate=float(fee_rate) / 100,
        )
        result = run_backtest(candles, config)
        paths = save_backtest_result(result)
        result["saved_paths"] = paths
        return result


backtest_manager = BacktestManager()
