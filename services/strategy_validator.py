from __future__ import annotations


class StrategyValidator:
    """Risk and configuration validator for strategy definitions."""

    def validate(self, strategy: dict) -> dict:
        warnings: list[str] = []
        errors: list[str] = []

        name = strategy.get("name", "").strip()
        if not name:
            errors.append("전략명이 비어 있습니다.")

        rules = strategy.get("rules", {})
        if not rules.get("entry"):
            errors.append("진입 조건이 없습니다.")
        if not rules.get("exit"):
            warnings.append("청산 조건이 부족합니다.")

        risk = strategy.get("risk", {})
        stop_loss = self._to_float(risk.get("stop_loss"), 0)
        take_profit = self._to_float(risk.get("take_profit"), 0)
        leverage = self._to_float(risk.get("leverage"), 1)
        max_ratio = self._to_float(risk.get("max_position_ratio"), 100)
        daily_loss = self._to_float(risk.get("daily_max_loss"), 100)

        if stop_loss <= 0:
            errors.append("손절값은 0보다 커야 합니다.")
        if take_profit <= 0:
            errors.append("익절값은 0보다 커야 합니다.")
        if stop_loss > 5:
            warnings.append("손절폭이 큽니다. 급격한 손실 가능성을 확인하세요.")
        if leverage > 5:
            warnings.append("레버리지가 높습니다. 실거래 전 모의검증이 필요합니다.")
        if max_ratio > 50:
            warnings.append("최대 투자 비율이 높습니다.")
        if daily_loss > 15:
            warnings.append("일 최대 손실 한도가 큽니다.")

        score = 100
        score -= len(errors) * 25
        score -= len(warnings) * 8
        score = max(0, min(100, score))

        return {
            "ok": not errors,
            "score": score,
            "errors": errors,
            "warnings": warnings,
        }

    @staticmethod
    def _to_float(value, default=0.0) -> float:
        try:
            return float(value)
        except Exception:
            return float(default)
