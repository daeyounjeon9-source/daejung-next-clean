from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime


class StrategyBuilder:
    """Simple rule-based strategy builder for DAEJUNG NEXT."""

    def __init__(self, strategy_dir: str | Path = "data/strategies"):
        self.strategy_dir = Path(strategy_dir)
        self.strategy_dir.mkdir(parents=True, exist_ok=True)

    def default_strategy(self) -> dict:
        return {
            "name": "EMA_RSI_SAMPLE",
            "description": "EMA trend filter + RSI entry sample strategy.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "rules": {
                "entry": [
                    {"left": "EMA20", "operator": ">", "right": "EMA60"},
                    {"left": "RSI14", "operator": "<", "right": 35},
                ],
                "exit": [
                    {"left": "profit_rate", "operator": ">=", "right": 5},
                    {"left": "loss_rate", "operator": "<=", "right": -2},
                ],
            },
            "risk": {
                "take_profit": 5.0,
                "stop_loss": 2.0,
                "leverage": 3,
                "max_position_ratio": 30,
                "daily_max_loss": 10,
            },
            "status": "draft",
        }

    def save_strategy(self, strategy: dict) -> Path:
        name = strategy.get("name", "strategy").strip().replace(" ", "_")
        if not name:
            name = "strategy"
        strategy["updated_at"] = datetime.now().isoformat(timespec="seconds")
        path = self.strategy_dir / f"{name}.json"
        path.write_text(json.dumps(strategy, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_strategy(self, name: str) -> dict:
        path = self.strategy_dir / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Strategy not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_strategies(self) -> list[str]:
        return sorted(p.stem for p in self.strategy_dir.glob("*.json"))

    def delete_strategy(self, name: str) -> bool:
        path = self.strategy_dir / f"{name}.json"
        if path.exists():
            path.unlink()
            return True
        return False
