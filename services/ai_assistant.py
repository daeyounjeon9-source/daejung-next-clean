from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

try:
    from services.strategy_validator import StrategyValidator
except Exception:
    from strategy_validator import StrategyValidator


class AIStrategyAssistant:
    """Local rule-based AI assistant placeholder.

    This module does not call external AI services. It provides deterministic
    strategy checks and suggestions so the program remains safe/offline.
    """

    def __init__(self, report_dir: str | Path = "data/ai_reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.validator = StrategyValidator()

    def analyze(self, strategy: dict) -> dict:
        validation = self.validator.validate(strategy)
        risk = strategy.get("risk", {})

        suggestions: list[str] = []
        leverage = self._to_float(risk.get("leverage"), 1)
        stop_loss = self._to_float(risk.get("stop_loss"), 0)
        take_profit = self._to_float(risk.get("take_profit"), 0)

        if leverage > 3:
            suggestions.append("레버리지를 3x 이하로 낮추는 것을 우선 검토하세요.")
        if stop_loss >= take_profit and take_profit > 0:
            suggestions.append("익절폭이 손절폭보다 충분히 큰지 확인하세요.")
        if stop_loss > 3:
            suggestions.append("손절폭을 1.5~3% 범위에서 다시 테스트하세요.")
        if not suggestions:
            suggestions.append("현재 설정은 기본 위험 기준을 통과했습니다. 백테스트로 추가 검증하세요.")

        risk_score = 100 - validation["score"]
        if risk_score < 30:
            level = "LOW"
        elif risk_score < 60:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "strategy_name": strategy.get("name", ""),
            "strategy_score": validation["score"],
            "risk_score": risk_score,
            "risk_level": level,
            "errors": validation["errors"],
            "warnings": validation["warnings"],
            "suggestions": suggestions,
        }

    def save_report(self, report: dict) -> Path:
        name = report.get("strategy_name") or "strategy"
        safe_name = name.strip().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.report_dir / f"{safe_name}_ai_report_{timestamp}.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    @staticmethod
    def _to_float(value, default=0.0) -> float:
        try:
            return float(value)
        except Exception:
            return float(default)
