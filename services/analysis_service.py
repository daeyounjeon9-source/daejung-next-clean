from __future__ import annotations

from typing import Any, Dict, List


def calculate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    profits = [float(r.get('profit_rate', 0) or 0) for r in results]
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]
    win_rate = (len(wins) / total * 100) if total else 0
    cumulative = sum(profits)
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss else (gross_profit if gross_profit else 0)

    equity = 0.0
    peak = 0.0
    mdd = 0.0
    for p in reversed(profits):
        equity += p
        peak = max(peak, equity)
        mdd = min(mdd, equity - peak)

    return {
        'total_trades': total,
        'wins': len(wins),
        'losses': len(losses),
        'win_rate': round(win_rate, 2),
        'cumulative_profit': round(cumulative, 2),
        'avg_win': round(sum(wins) / len(wins), 2) if wins else 0,
        'avg_loss': round(sum(losses) / len(losses), 2) if losses else 0,
        'max_win': round(max(profits), 2) if profits else 0,
        'max_loss': round(min(profits), 2) if profits else 0,
        'profit_factor': round(profit_factor, 2),
        'mdd': round(mdd, 2),
    }


def filter_results(results: List[Dict[str, Any]], keyword: str = '', symbol: str = '', strategy: str = '') -> List[Dict[str, Any]]:
    keyword = keyword.strip().lower()
    symbol = symbol.strip().lower()
    strategy = strategy.strip().lower()
    filtered = []
    for row in results:
        text = ' '.join(str(v).lower() for v in row.values())
        if keyword and keyword not in text:
            continue
        if symbol and symbol not in str(row.get('symbol', '')).lower():
            continue
        if strategy and strategy not in str(row.get('strategy', '')).lower():
            continue
        filtered.append(row)
    return filtered
