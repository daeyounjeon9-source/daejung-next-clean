import json
import tkinter as tk
from pathlib import Path

from core.log_manager import add_log
from core.state_manager import state_manager

RESULT_DIR = Path(__file__).resolve().parents[1] / "data" / "results"


class AnalysisPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.summary_cards = {}
        self._build()
        self.refresh()

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="결과분석",
            font=("Malgun Gothic", 20, "bold"),
            anchor="w"
        ).pack(side="left")

        tk.Label(
            header,
            text="거래 결과 / 수익률 / 승률 분석 화면",
            font=("Malgun Gothic", 10),
            anchor="e"
        ).pack(side="right")

        filter_frame = tk.LabelFrame(self, text="조회 조건", padx=12, pady=10)
        filter_frame.pack(fill="x", padx=20, pady=8)

        tk.Label(filter_frame, text="기간").pack(side="left", padx=(0, 6))
        self.period_var = tk.StringVar(value="오늘")
        tk.OptionMenu(filter_frame, self.period_var, "오늘", "7일", "30일", "전체").pack(side="left", padx=(0, 18))

        tk.Label(filter_frame, text="전략").pack(side="left", padx=(0, 6))
        self.strategy_var = tk.StringVar(value="전체")
        tk.OptionMenu(filter_frame, self.strategy_var, "전체", "EMA Cross", "RSI", "MACD", "Custom Strategy").pack(side="left", padx=(0, 18))

        tk.Label(filter_frame, text="종목").pack(side="left", padx=(0, 6))
        self.symbol_var = tk.StringVar(value="전체")
        tk.OptionMenu(filter_frame, self.symbol_var, "전체", "BTCUSDT", "ETHUSDT", "KRW-BTC").pack(side="left", padx=(0, 18))

        tk.Button(filter_frame, text="새로고침", width=14, command=self.refresh).pack(side="right")

        summary_frame = tk.LabelFrame(self, text="요약 통계", padx=12, pady=10)
        summary_frame.pack(fill="x", padx=20, pady=8)

        cards = [
            ("total", "총 거래수"),
            ("success", "성공 거래"),
            ("fail", "실패 거래"),
            ("win_rate", "승률"),
            ("profit", "누적 수익률"),
        ]

        for i, (key, title) in enumerate(cards):
            box = tk.LabelFrame(summary_frame, text=title, width=150, height=72, padx=8, pady=6)
            box.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            box.grid_propagate(False)

            val = tk.Label(box, text="-", font=("Malgun Gothic", 12, "bold"))
            val.pack(expand=True)

            self.summary_cards[key] = val
            summary_frame.columnconfigure(i, weight=1)

        chart = tk.LabelFrame(self, text="차트 영역", padx=12, pady=14)
        chart.pack(fill="x", padx=20, pady=8)

        self.chart_label = tk.Label(
            chart,
            text="수익률 / 자산 변화 그래프 위치\n현재는 결과 데이터 누적 후 차트 연결 예정",
            height=4,
            font=("Malgun Gothic", 11)
        )
        self.chart_label.pack(fill="x")

        table = tk.LabelFrame(self, text="최근 거래내역", padx=8, pady=8)
        table.pack(fill="both", expand=True, padx=20, pady=(8, 20))

        self.text = tk.Text(table, height=12)
        self.text.pack(fill="both", expand=True)

    def load_results(self):
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        rows = []

        for path in sorted(RESULT_DIR.glob("*.json")):
            try:
                rows.append(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                pass

        return rows

    def refresh(self):
        rows = self.load_results()

        total = len(rows)
        success = sum(1 for r in rows if r.get("result") == "성공")
        fail = total - success
        profit = sum(float(r.get("profit_rate", 0) or 0) for r in rows)
        win = (success / total * 100) if total else 0

        values = {
            "total": f"{total}회",
            "success": f"{success}회",
            "fail": f"{fail}회",
            "win_rate": f"{win:.2f}%",
            "profit": f"{profit:.2f}%",
        }

        for key, value in values.items():
            self.summary_cards[key].config(text=value)

        state_manager.update_state({
            "trade_count": total,
            "today_profit": profit,
            "total_profit": profit,
            "win_rate": win,
        })

        add_log("결과분석: 거래 결과 새로고침 완료", "INFO")

        self.text.delete("1.0", "end")
        self.text.insert("end", "시간\t\t종목\t방향\t결과\t수익률\n")
        self.text.insert("end", "-" * 70 + "\n")

        if not rows:
            self.text.insert("end", "아직 거래 결과 데이터가 없습니다.\n")
            self.text.insert("end", f"결과 저장 경로: {RESULT_DIR}\n")
            return

        for r in rows[-80:]:
            self.text.insert(
                "end",
                f"{r.get('time', '-')}\t{r.get('symbol', '-')}\t{r.get('side', '-')}\t"
                f"{r.get('result', '-')}\t{r.get('profit_rate', 0)}%\n"
            )