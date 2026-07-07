from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "backtest" / "reports"
DATA_DIR = BASE_DIR / "data" / "backtests"


def save_backtest_result(result: dict) -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = DATA_DIR / f"backtest_{stamp}.json"
    csv_path = REPORT_DIR / f"backtest_trades_{stamp}.csv"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    trades = result.get("trades", [])
    if trades:
        with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(trades[0].keys()))
            writer.writeheader()
            writer.writerows(trades)
    else:
        csv_path.write_text("no trades\n", encoding="utf-8-sig")
    return {"json": str(json_path), "csv": str(csv_path)}
