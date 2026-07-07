from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


@dataclass
class StrategySuggestion:
    risk_level: str
    bias: str
    summary: str
    checklist: list[str]
    warnings: list[str]
    created_at: str


class AIStrategyService:
    """Offline rule-based AI assistant placeholder.

    This module does not call external AI APIs. It reviews the user's strategy
    settings and recent backtest-style numbers, then creates a practical
    checklist before simulated trading.
    """

    def __init__(self, report_dir: str = "data/ai_reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def analyze(self, strategy: str, symbol: str, amount: float, leverage: float,
                stop_loss: float, take_profit: float, win_rate: float = 0.0,
                total_profit: float = 0.0) -> StrategySuggestion:
        warnings: list[str] = []
        checklist: list[str] = []

        rr = (take_profit / stop_loss) if stop_loss else 0
        risk_score = 0
        if leverage >= 10:
            risk_score += 3
            warnings.append("레버리지가 높습니다. 실거래 전 모의 실행을 먼저 권장합니다.")
        elif leverage >= 5:
            risk_score += 2
        else:
            risk_score += 1

        if stop_loss <= 0:
            risk_score += 3
            warnings.append("손절 값이 없거나 0입니다. 실행 전 손절 기준을 설정하세요.")
        if rr and rr < 1:
            risk_score += 2
            warnings.append("익절/손절 비율이 1보다 낮습니다. 기대수익 구조를 재검토하세요.")
        if amount <= 0:
            warnings.append("투자금이 설정되지 않았습니다.")
        if not symbol:
            warnings.append("종목이 비어 있습니다.")
        if not strategy:
            warnings.append("전략이 선택되지 않았습니다.")

        if win_rate >= 60 and total_profit > 0:
            bias = "긍정"
            checklist.append("최근 결과가 양호합니다. 동일 조건으로 추가 백테스트를 진행하세요.")
        elif win_rate > 0:
            bias = "중립"
            checklist.append("승률과 누적수익을 함께 확인하세요. 승률만으로 실행하지 마세요.")
        else:
            bias = "검증 필요"
            checklist.append("백테스트 결과가 부족합니다. 먼저 백테스트를 실행하세요.")

        checklist.extend([
            "API 연결 상태를 확인하세요.",
            "실거래 전 안전모드가 켜져 있는지 확인하세요.",
            "최대 손실 허용 범위를 먼저 정하세요.",
            "모의 실행 결과가 분석 페이지에 저장되는지 확인하세요.",
        ])

        if risk_score >= 6:
            risk_level = "높음"
        elif risk_score >= 3:
            risk_level = "중간"
        else:
            risk_level = "낮음"

        summary = f"{symbol or '미지정'} / {strategy or '미선택'} 전략은 현재 위험도 {risk_level}, 판단은 {bias}입니다."
        return StrategySuggestion(risk_level, bias, summary, checklist, warnings, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def save_report(self, suggestion: StrategySuggestion) -> str:
        path = self.report_dir / f"ai_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(asdict(suggestion), ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)
