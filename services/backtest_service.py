from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BacktestConfig:
    strategy: str = "EMA Cross"
    symbol: str = "BTCUSDT"
    initial_balance: float = 10_000_000
    fee_rate: float = 0.0005
    short_window: int = 5
    long_window: int = 20


def _sma(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return sum(values[-window:]) / window


def run_backtest(candles: list[dict], config: BacktestConfig | None = None) -> dict:
    config = config or BacktestConfig()
    balance = float(config.initial_balance)
    equity_curve = []
    trades = []
    closes = []
    position = None

    for candle in candles:
        close = float(candle["close"])
        closes.append(close)
        fast = _sma(closes, config.short_window)
        slow = _sma(closes, config.long_window)
        if fast is None or slow is None:
            equity_curve.append(balance)
            continue

        if position is None and fast > slow:
            qty = balance / close
            fee = balance * config.fee_rate
            position = {"entry_time": candle["time"], "entry_price": close, "qty": qty, "fee_in": fee}
            balance -= fee
        elif position is not None and fast < slow:
            gross = position["qty"] * close
            entry_value = position["qty"] * position["entry_price"]
            fee_out = gross * config.fee_rate
            pnl = gross - entry_value - position["fee_in"] - fee_out
            pnl_rate = pnl / max(entry_value, 1) * 100
            balance = balance + pnl
            trades.append({
                "entry_time": position["entry_time"],
                "exit_time": candle["time"],
                "symbol": config.symbol,
                "strategy": config.strategy,
                "side": "LONG",
                "entry_price": round(position["entry_price"], 2),
                "exit_price": round(close, 2),
                "profit": round(pnl, 2),
                "profit_rate": round(pnl_rate, 4),
                "result": "WIN" if pnl >= 0 else "LOSS",
            })
            position = None
        equity_curve.append(balance)

    if position is not None and candles:
        close = float(candles[-1]["close"])
        gross = position["qty"] * close
        entry_value = position["qty"] * position["entry_price"]
        fee_out = gross * config.fee_rate
        pnl = gross - entry_value - position["fee_in"] - fee_out
        balance = balance + pnl
        trades.append({
            "entry_time": position["entry_time"],
            "exit_time": candles[-1]["time"],
            "symbol": config.symbol,
            "strategy": config.strategy,
            "side": "LONG",
            "entry_price": round(position["entry_price"], 2),
            "exit_price": round(close, 2),
            "profit": round(pnl, 2),
            "profit_rate": round(pnl / max(entry_value, 1) * 100, 4),
            "result": "WIN" if pnl >= 0 else "LOSS",
        })

    total = len(trades)
    wins = sum(1 for t in trades if t["profit"] >= 0)
    losses = total - wins
    total_profit = sum(t["profit"] for t in trades)
    win_rate = (wins / total * 100) if total else 0
    cumulative_rate = ((balance - config.initial_balance) / config.initial_balance * 100) if config.initial_balance else 0
    peak = config.initial_balance
    max_drawdown = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        dd = (peak - value) / peak * 100 if peak else 0
        max_drawdown = max(max_drawdown, dd)

    return {
        "config": config.__dict__,
        "summary": {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
            "initial_balance": round(config.initial_balance, 2),
            "final_balance": round(balance, 2),
            "total_profit": round(total_profit, 2),
            "cumulative_rate": round(cumulative_rate, 2),
            "mdd": round(max_drawdown, 2),
        },
        "equity_curve": [round(x, 2) for x in equity_curve],
        "trades": trades,
    }
