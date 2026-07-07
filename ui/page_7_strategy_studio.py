from __future__ import annotations

import json
from pathlib import Path

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
        QTextEdit, QComboBox, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
        QListWidget, QMessageBox
    )
    from PySide6.QtCore import Qt
except Exception:
    # This file is intended for PySide6 projects. Import failure is handled by main app.
    pass

from services.strategy_builder import StrategyBuilder
from services.ai_assistant import AIStrategyAssistant


class StrategyStudioPage(QWidget):
    """DAEJUNG NEXT Sprint 8 - Strategy Studio page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.builder = StrategyBuilder()
        self.ai = AIStrategyAssistant()
        self.current_strategy = self.builder.default_strategy()
        self._build_ui()
        self.refresh_strategy_list()
        self.load_to_form(self.current_strategy)

    def _build_ui(self):
        root = QHBoxLayout(self)

        left_box = QGroupBox("전략 목록")
        left_layout = QVBoxLayout(left_box)
        self.strategy_list = QListWidget()
        self.strategy_list.itemClicked.connect(self.on_strategy_selected)
        left_layout.addWidget(self.strategy_list)

        btn_new = QPushButton("새 전략")
        btn_save = QPushButton("저장")
        btn_delete = QPushButton("삭제")
        btn_refresh = QPushButton("새로고침")
        btn_new.clicked.connect(self.new_strategy)
        btn_save.clicked.connect(self.save_strategy)
        btn_delete.clicked.connect(self.delete_strategy)
        btn_refresh.clicked.connect(self.refresh_strategy_list)

        left_layout.addWidget(btn_new)
        left_layout.addWidget(btn_save)
        left_layout.addWidget(btn_delete)
        left_layout.addWidget(btn_refresh)

        center_box = QGroupBox("전략 빌더")
        form = QFormLayout(center_box)

        self.name_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(60)

        self.entry_left = QComboBox()
        self.entry_left.addItems(["EMA20", "EMA60", "RSI14", "MACD", "PRICE"])
        self.entry_op = QComboBox()
        self.entry_op.addItems([">", "<", ">=", "<=", "=="])
        self.entry_right = QLineEdit("EMA60")

        self.rsi_limit = QSpinBox()
        self.rsi_limit.setRange(1, 99)
        self.rsi_limit.setValue(35)

        self.take_profit = QDoubleSpinBox()
        self.take_profit.setRange(0.1, 100)
        self.take_profit.setValue(5.0)
        self.take_profit.setSuffix(" %")

        self.stop_loss = QDoubleSpinBox()
        self.stop_loss.setRange(0.1, 100)
        self.stop_loss.setValue(2.0)
        self.stop_loss.setSuffix(" %")

        self.leverage = QSpinBox()
        self.leverage.setRange(1, 125)
        self.leverage.setValue(3)
        self.leverage.setSuffix(" x")

        self.max_ratio = QSpinBox()
        self.max_ratio.setRange(1, 100)
        self.max_ratio.setValue(30)
        self.max_ratio.setSuffix(" %")

        form.addRow("전략명", self.name_edit)
        form.addRow("설명", self.desc_edit)
        form.addRow("조건 왼쪽", self.entry_left)
        form.addRow("조건 연산", self.entry_op)
        form.addRow("조건 오른쪽", self.entry_right)
        form.addRow("RSI 기준", self.rsi_limit)
        form.addRow("익절", self.take_profit)
        form.addRow("손절", self.stop_loss)
        form.addRow("레버리지", self.leverage)
        form.addRow("최대 투자비율", self.max_ratio)

        action_row = QHBoxLayout()
        btn_ai = QPushButton("AI 점검")
        btn_report = QPushButton("보고서 저장")
        btn_ai.clicked.connect(self.run_ai_check)
        btn_report.clicked.connect(self.save_ai_report)
        action_row.addWidget(btn_ai)
        action_row.addWidget(btn_report)
        form.addRow(action_row)

        right_box = QGroupBox("AI 전략 점검 결과")
        right_layout = QVBoxLayout(right_box)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        right_layout.addWidget(self.result_text)

        root.addWidget(left_box, 1)
        root.addWidget(center_box, 2)
        root.addWidget(right_box, 2)

    def form_to_strategy(self) -> dict:
        strategy = self.current_strategy.copy()
        strategy["name"] = self.name_edit.text().strip() or "NEW_STRATEGY"
        strategy["description"] = self.desc_edit.toPlainText().strip()
        strategy["rules"] = {
            "entry": [
                {
                    "left": self.entry_left.currentText(),
                    "operator": self.entry_op.currentText(),
                    "right": self.entry_right.text().strip(),
                },
                {"left": "RSI14", "operator": "<", "right": self.rsi_limit.value()},
            ],
            "exit": [
                {"left": "profit_rate", "operator": ">=", "right": self.take_profit.value()},
                {"left": "loss_rate", "operator": "<=", "right": -self.stop_loss.value()},
            ],
        }
        strategy["risk"] = {
            "take_profit": self.take_profit.value(),
            "stop_loss": self.stop_loss.value(),
            "leverage": self.leverage.value(),
            "max_position_ratio": self.max_ratio.value(),
            "daily_max_loss": 10,
        }
        return strategy

    def load_to_form(self, strategy: dict):
        self.current_strategy = strategy
        self.name_edit.setText(strategy.get("name", ""))
        self.desc_edit.setPlainText(strategy.get("description", ""))
        risk = strategy.get("risk", {})
        self.take_profit.setValue(float(risk.get("take_profit", 5)))
        self.stop_loss.setValue(float(risk.get("stop_loss", 2)))
        self.leverage.setValue(int(risk.get("leverage", 3)))
        self.max_ratio.setValue(int(risk.get("max_position_ratio", 30)))

    def refresh_strategy_list(self):
        self.strategy_list.clear()
        for name in self.builder.list_strategies():
            self.strategy_list.addItem(name)

    def new_strategy(self):
        self.load_to_form(self.builder.default_strategy())
        self.result_text.setPlainText("새 전략을 작성하세요.")

    def save_strategy(self):
        strategy = self.form_to_strategy()
        path = self.builder.save_strategy(strategy)
        self.current_strategy = strategy
        self.refresh_strategy_list()
        QMessageBox.information(self, "저장 완료", f"전략 저장 완료:\n{path}")

    def delete_strategy(self):
        name = self.name_edit.text().strip()
        if not name:
            return
        if self.builder.delete_strategy(name):
            self.refresh_strategy_list()
            self.new_strategy()

    def on_strategy_selected(self, item):
        strategy = self.builder.load_strategy(item.text())
        self.load_to_form(strategy)

    def run_ai_check(self):
        report = self.ai.analyze(self.form_to_strategy())
        self.result_text.setPlainText(json.dumps(report, ensure_ascii=False, indent=2))

    def save_ai_report(self):
        report = self.ai.analyze(self.form_to_strategy())
        path = self.ai.save_report(report)
        self.result_text.setPlainText(json.dumps(report, ensure_ascii=False, indent=2))
        QMessageBox.information(self, "보고서 저장 완료", f"AI 전략 보고서 저장:\n{path}")
