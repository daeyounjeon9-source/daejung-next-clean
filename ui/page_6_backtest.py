from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QGroupBox, QFormLayout
)

from core.backtest_manager import backtest_manager


class BacktestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.last_result = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        title = QLabel("6 백테스트 & 전략 검증")
        title.setStyleSheet("font-size:20px; font-weight:bold; padding:8px;")
        root.addWidget(title)

        box = QGroupBox("백테스트 설정")
        form = QFormLayout(box)
        self.strategy = QComboBox(); self.strategy.addItems(["EMA Cross", "RSI", "MACD", "Custom Strategy"])
        self.symbol = QComboBox(); self.symbol.addItems(["BTCUSDT", "ETHUSDT", "XRPUSDT", "SOLUSDT"])
        self.initial = QLineEdit("10000000")
        self.fee = QLineEdit("0.05")
        self.count = QLineEdit("300")
        form.addRow("전략", self.strategy)
        form.addRow("종목", self.symbol)
        form.addRow("초기자금", self.initial)
        form.addRow("수수료(%)", self.fee)
        form.addRow("캔들 개수", self.count)
        root.addWidget(box)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("백테스트 시작")
        self.start_btn.clicked.connect(self.run_backtest)
        btn_row.addWidget(self.start_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

        self.summary = QLabel("대기 중")
        self.summary.setStyleSheet("font-size:14px; padding:8px; background:#f5f5f5;")
        root.addWidget(self.summary)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["진입시간", "청산시간", "종목", "방향", "진입가", "청산가", "수익", "결과"])
        root.addWidget(self.table, 1)

        self.log = QTextEdit(); self.log.setReadOnly(True); self.log.setFixedHeight(110)
        root.addWidget(self.log)

    def run_backtest(self):
        try:
            self.log.append("백테스트 시작")
            result = backtest_manager.run(
                strategy=self.strategy.currentText(),
                symbol=self.symbol.currentText(),
                initial_balance=float(self.initial.text()),
                fee_rate=float(self.fee.text()),
                candle_count=int(self.count.text()),
            )
            self.last_result = result
            self._render_result(result)
            self.log.append("백테스트 완료")
            self.log.append(f"저장: {result.get('saved_paths', {})}")
        except Exception as exc:
            self.log.append(f"오류: {exc}")

    def _render_result(self, result: dict):
        s = result.get("summary", {})
        self.summary.setText(
            f"총거래 {s.get('total_trades', 0)} | 승률 {s.get('win_rate', 0)}% | "
            f"누적수익률 {s.get('cumulative_rate', 0)}% | MDD {s.get('mdd', 0)}% | "
            f"최종자산 {s.get('final_balance', 0):,.0f}"
        )
        trades = result.get("trades", [])
        self.table.setRowCount(len(trades))
        for r, t in enumerate(trades):
            values = [
                t.get("entry_time", ""), t.get("exit_time", ""), t.get("symbol", ""), t.get("side", ""),
                str(t.get("entry_price", "")), str(t.get("exit_price", "")),
                f"{t.get('profit', 0):,.2f}", t.get("result", ""),
            ]
            for c, value in enumerate(values):
                self.table.setItem(r, c, QTableWidgetItem(value))

    def refresh(self):
        pass
