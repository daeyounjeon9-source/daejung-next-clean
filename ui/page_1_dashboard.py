import tkinter as tk
from datetime import datetime

from core.event_bus import event_bus
from core.log_manager import add_log, get_logs
from core.state_manager import state_manager


class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cards = {}
        self.card_boxes = {}
        self._build()
        self.refresh()
        event_bus.subscribe("state_changed", self._on_state_changed)

    def _on_state_changed(self, _data=None):
        self.refresh()

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(header, text="메인 대시보드", font=("Malgun Gothic", 21, "bold")).pack(side="left")
        self.clock_label = tk.Label(header, text="", font=("Malgun Gothic", 10))
        self.clock_label.pack(side="right")

        top_status = tk.LabelFrame(self, text="현재 운영 상태", padx=10, pady=8)
        top_status.pack(fill="x", padx=20, pady=(0, 10))

        top_items = [
            ("current_project", "프로젝트"),
            ("api_status", "API"),
            ("run_status", "실행"),
            ("current_strategy", "전략"),
        ]

        for i, (key, title) in enumerate(top_items):
            box = tk.LabelFrame(top_status, text=title, width=210, height=64, padx=8, pady=5)
            box.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            box.grid_propagate(False)
            value = tk.Label(box, text="-", font=("Malgun Gothic", 13, "bold"))
            value.pack(expand=True)
            self.cards[key] = value
            self.card_boxes[key] = box
            top_status.columnconfigure(i, weight=1)

        grid = tk.LabelFrame(self, text="핵심 지표", padx=10, pady=8)
        grid.pack(fill="x", padx=20)

        items = [
            ("exchange", "거래소"),
            ("current_symbol", "현재 종목"),
            ("current_position", "현재 포지션"),
            ("total_asset", "총 자산"),
            ("today_profit", "오늘 손익"),
            ("total_profit", "누적 손익"),
            ("trade_count", "거래횟수"),
            ("win_rate", "승률"),
            ("runtime", "실행시간"),
            ("server_time", "서버시간"),
            ("cpu_status", "CPU"),
            ("memory_status", "메모리"),
        ]

        for i, (key, title) in enumerate(items):
            box = tk.LabelFrame(grid, text=title, width=170, height=72, padx=8, pady=6)
            box.grid(row=i // 4, column=i % 4, padx=6, pady=6, sticky="nsew")
            box.grid_propagate(False)
            value = tk.Label(box, text="-", font=("Malgun Gothic", 12, "bold"))
            value.pack(expand=True)
            self.cards[key] = value
            self.card_boxes[key] = box

        for col in range(4):
            grid.columnconfigure(col, weight=1)

        quick = tk.LabelFrame(self, text="빠른 실행", padx=12, pady=10)
        quick.pack(fill="x", padx=20, pady=12)

        buttons = [
            ("API 연결", self._mock_api_connect),
            ("프로젝트 선택", lambda: self._log_only("프로젝트 선택은 입력센터에서 진행")),
            ("전략 선택", lambda: self._log_only("전략 선택은 입력센터에서 진행")),
            ("실행", self._mock_start),
            ("중지", self._mock_stop),
            ("백테스트", lambda: self._log_only("백테스트 준비")),
            ("설정", lambda: self._log_only("설정 화면은 시스템관리에서 진행")),
            ("새로고침", self.refresh),
        ]

        for text, cmd in buttons:
            tk.Button(quick, text=text, width=14, height=1, command=cmd).pack(side="left", padx=5, pady=3)

        middle = tk.Frame(self)
        middle.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        memo_frame = tk.LabelFrame(middle, text="운영 메모", padx=10, pady=8)
        memo_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.memo = tk.Text(memo_frame, height=10)
        self.memo.pack(fill="both", expand=True)

        log_frame = tk.LabelFrame(middle, text="최근 상태 로그", padx=10, pady=8)
        log_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.log_box = tk.Text(log_frame, height=10)
        self.log_box.pack(fill="both", expand=True)

    def _log_only(self, message):
        add_log(message, "INFO")
        self.refresh()

    def _mock_api_connect(self):
        state_manager.update_state({
            "api_status": "ONLINE",
            "exchange": "테스트 거래소"
        })
        add_log("API 연결 상태를 ONLINE으로 변경", "SUCCESS")
        self.refresh()

    def _mock_start(self):
        state_manager.update_state({
            "run_status": "RUNNING",
            "runtime": "00:00:00"
        })
        add_log("대시보드 빠른 실행 시작", "INFO")
        self.refresh()

    def _mock_stop(self):
        state_manager.update_state({
            "run_status": "READY",
            "current_position": "없음"
        })
        add_log("대시보드 빠른 실행 중지", "WARNING")
        self.refresh()

    def _system_status(self):
        try:
            import psutil
            return f"{psutil.cpu_percent()}%", f"{psutil.virtual_memory().percent}%"
        except Exception:
            return "대기", "대기"

    def _set_card_color(self, key, value):
        color = "SystemButtonFace"
        text = str(value).upper()

        if text in ["ONLINE", "RUNNING", "실행중"]:
            color = "#d8f5d0"
        elif text in ["OFFLINE", "ERROR", "FAILED", "긴급정지"]:
            color = "#ffd6d6"
        elif text in ["READY", "대기", "정지", "일시정지"]:
            color = "#fff1bf"
        elif text in ["없음", "-", "미선택"]:
            color = "#eeeeee"

        if key in self.cards:
            self.cards[key].config(bg=color)
        if key in self.card_boxes:
            self.card_boxes[key].config(bg=color)

    def refresh(self):
        s = state_manager.get_state()
        now = datetime.now()
        cpu_status, memory_status = self._system_status()

        values = {
            "current_project": s.get("current_project") or "기본",
            "api_status": s.get("api_status", "OFFLINE"),
            "run_status": s.get("run_status", "READY"),
            "current_strategy": s.get("current_strategy", "없음"),
            "exchange": s.get("exchange") or "미선택",
            "current_symbol": s.get("current_symbol", "-"),
            "current_position": s.get("current_position", "없음"),
            "total_asset": s.get("total_asset", "0 KRW"),
            "today_profit": f"{float(s.get('today_profit', 0.0)):.2f}%",
            "total_profit": f"{float(s.get('total_profit', 0.0)):.2f}%",
            "trade_count": f"{s.get('trade_count', 0)}회",
            "win_rate": f"{float(s.get('win_rate', 0.0)):.1f}%",
            "runtime": s.get("runtime", "00:00:00"),
            "server_time": now.strftime("%H:%M:%S"),
            "cpu_status": cpu_status,
            "memory_status": memory_status,
        }

        for key, value in values.items():
            if key in self.cards:
                self.cards[key].config(text=value)
                self._set_card_color(key, value)

        self.clock_label.config(
            text=f"대정NEXT 운영 상태판 | {now.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        self.memo.delete("1.0", "end")
        self.memo.insert("end", "대정NEXT Sprint 2\n")
        self.memo.insert("end", "- 메인 대시보드 연결공사 적용\n")
        self.memo.insert("end", "- state_changed 이벤트 수신 연결\n")
        self.memo.insert("end", "- 자동 1초 갱신 제거로 깜박임 방지\n")
        self.memo.insert("end", "- 저장/실행/분석 변경 시 대시보드 반영\n")
        self.memo.insert("end", f"- 마지막 갱신: {now.strftime('%H:%M:%S')}\n")

        self.log_box.delete("1.0", "end")
        logs = get_logs(50)
        self.log_box.insert("end", "\n".join(logs) if logs else "아직 로그가 없습니다.")