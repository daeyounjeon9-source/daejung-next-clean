from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "backtest" / "datasets"


def generate_sample_candles(symbol: str = "BTCUSDT", count: int = 300, start_price: float = 65000.0) -> list[dict]:
    candles = []
    price = start_price
    start_time = datetime.now() - timedelta(minutes=count)
    for i in range(count):
        open_price = price
        move = random.uniform(-120, 140)
        close_price = max(1, open_price + move)
        high_price = max(open_price, close_price) + random.uniform(5, 60)
        low_price = min(open_price, close_price) - random.uniform(5, 60)
        volume = random.uniform(10, 250)
        candles.append({
            "time": (start_time + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": round(volume, 4),
        })
        price = close_price
    return candles


def load_csv_candles(symbol: str) -> list[dict]:
    path = DATASET_DIR / symbol / "candles.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append({
                "time": row.get("time", ""),
                "symbol": symbol,
                "open": float(row.get("open", 0)),
                "high": float(row.get("high", 0)),
                "low": float(row.get("low", 0)),
                "close": float(row.get("close", 0)),
                "volume": float(row.get("volume", 0)),
            })
        return rows


def load_candles(symbol: str = "BTCUSDT", count: int = 300) -> list[dict]:
    rows = load_csv_candles(symbol)
    if rows:
        return rows
    return generate_sample_candles(symbol=symbol, count=count)
