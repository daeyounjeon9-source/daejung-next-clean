import tkinter as tk
from tkinter import ttk, messagebox

from services.ai_strategy_service import AIStrategyService
from core.log_manager import add_log


class AIStrategyPage(ttk.Frame):
    def __init__(self, parent, bottom_label=None):
        super().__init__(parent, padding=12)
        self.bottom_label = bottom_label
        self.service = AIStrategyService()
        self._build()

    def _build(self):
        ttk.Label(self, text="AI 전략 보조", font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="외부 AI API 없이 동작하는 안전 점검/전략 보조 초안입니다.").pack(anchor="w", pady=(0, 10))

        form = ttk.LabelFrame(self, text="전략 조건 입력", padding=10)
        form.pack(fill="x", pady=8)

        self.strategy = tk.StringVar(value="스캘핑")
        self.symbol = tk.StringVar(value="BTCUSDT")
        self.amount = tk.StringVar(value="100000")
        self.leverage = tk.StringVar(value="3")
        self.stop_loss = tk.StringVar(value="1.0")
        self.take_profit = tk.StringVar(value="1.5")
        self.win_rate = tk.StringVar(value="0")
        self.total_profit = tk.StringVar(value="0")

        rows = [
            ("전략", self.strategy), ("종목", self.symbol), ("투자금", self.amount),
            ("레버리지", self.leverage), ("손절 %", self.stop_loss), ("익절 %", self.take_profit),
            ("최근 승률 %", self.win_rate), ("최근 누적수익 %", self.total_profit),
        ]
        for i, (label, var) in enumerate(rows):
            ttk.Label(form, text=label).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)
            ttk.Entry(form, textvariable=var, width=24).grid(row=i//2, column=(i%2)*2+1, sticky="ew", padx=5, pady=4)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=8)
        ttk.Button(btns, text="전략 점검", command=self.run_analysis).pack(side="left", padx=4)
        ttk.Button(btns, text="보고서 저장", command=self.save_report).pack(side="left", padx=4)

        self.result_text = tk.Text(self, height=20, wrap="word")
        self.result_text.pack(fill="both", expand=True, pady=8)
        self.current_suggestion = None

    def _float(self, value, default=0.0):
        try:
            return float(value)
        except Exception:
            return default

    def run_analysis(self):
        self.current_suggestion = self.service.analyze(
            strategy=self.strategy.get().strip(),
            symbol=self.symbol.get().strip(),
            amount=self._float(self.amount.get()),
            leverage=self._float(self.leverage.get()),
            stop_loss=self._float(self.stop_loss.get()),
            take_profit=self._float(self.take_profit.get()),
            win_rate=self._float(self.win_rate.get()),
            total_profit=self._float(self.total_profit.get()),
        )
        s = self.current_suggestion
        lines = [
            f"생성 시간: {s.created_at}",
            f"요약: {s.summary}",
            f"위험도: {s.risk_level}",
            f"판단: {s.bias}",
            "",
            "체크리스트:",
            *[f"- {x}" for x in s.checklist],
            "",
            "경고:",
            *([f"- {x}" for x in s.warnings] or ["- 경고 없음"]),
        ]
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "\n".join(lines))
        line = add_log("AI 전략 점검 완료", "SUCCESS")
        if self.bottom_label:
            self.bottom_label.config(text=f"공통 로그: {line}")

    def save_report(self):
        if not self.current_suggestion:
            self.run_analysis()
        path = self.service.save_report(self.current_suggestion)
        line = add_log(f"AI 전략 보고서 저장: {path}", "SUCCESS")
        if self.bottom_label:
            self.bottom_label.config(text=f"공통 로그: {line}")
        messagebox.showinfo("저장 완료", f"보고서 저장 위치:\n{path}")
