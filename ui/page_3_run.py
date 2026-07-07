import tkinter as tk
from core.config_manager import load_config
from core.log_manager import get_logs, add_log
from core.state_manager import state_manager
from services.run_service import run_service


class RunPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.info = {}
        self.status_cards = {}
        self._build()
        self.refresh()

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="실행센터",
            font=("Malgun Gothic", 20, "bold"),
            anchor="w"
        ).pack(side="left")

        tk.Label(
            header,
            text="실행 / 정지 / 긴급정지 운영 화면",
            font=("Malgun Gothic", 10),
            anchor="e"
        ).pack(side="right")

        info_frame = tk.LabelFrame(self, text="현재 실행 정보", padx=12, pady=10)
        info_frame.pack(fill="x", padx=20, pady=8)

        items = [
            ("project", "프로젝트"),
            ("strategy", "전략"),
            ("symbol", "종목"),
            ("api", "API"),
            ("ready", "준비상태"),
        ]

        for i, (key, label) in enumerate(items):
            box = tk.LabelFrame(info_frame, text=label, width=165, height=70, padx=8, pady=6)
            box.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            box.grid_propagate(False)

            val = tk.Label(box, text="-", font=("Malgun Gothic", 12, "bold"))
            val.pack(expand=True)

            self.info[key] = val
            info_frame.columnconfigure(i, weight=1)

        control_frame = tk.LabelFrame(self, text="실행 제어", padx=12, pady=12)
        control_frame.pack(fill="x", padx=20, pady=8)

        controls = [
            ("▶ 실행", self.start_run),
            ("Ⅱ 일시정지", self.pause_run),
            ("■ 정지", self.stop_run),
            ("⚠ 긴급정지", self.emergency_stop),
            ("↻ 새로고침", self.refresh),
        ]

        for text, cmd in controls:
            tk.Button(
                control_frame,
                text=text,
                width=16,
                height=2,
                command=cmd
            ).pack(side="left", padx=7)

        status_frame = tk.LabelFrame(self, text="진행 상태", padx=12, pady=10)
        status_frame.pack(fill="x", padx=20, pady=8)

        self.progress = tk.Label(
            status_frame,
            text="[□□□□□□□□□□] 0%",
            font=("Malgun Gothic", 14, "bold"),
            anchor="w"
        )
        self.progress.pack(fill="x", pady=(0, 6))

        self.step = tk.Label(
            status_frame,
            text="현재 단계: 대기",
            font=("Malgun Gothic", 11),
            anchor="w"
        )
        self.step.pack(fill="x")

        card_frame = tk.LabelFrame(self, text="실시간 상태 카드", padx=12, pady=10)
        card_frame.pack(fill="x", padx=20, pady=8)

        cards = [
            ("run_status", "현재상태"),
            ("runtime", "실행시간"),
            ("current_profit", "현재수익"),
            ("current_position", "포지션"),
        ]

        for i, (key, title) in enumerate(cards):
            box = tk.LabelFrame(card_frame, text=title, width=190, height=72, padx=8, pady=6)
            box.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            box.grid_propagate(False)

            val = tk.Label(box, text="-", font=("Malgun Gothic", 12, "bold"))
            val.pack(expand=True)

            self.status_cards[key] = val
            card_frame.columnconfigure(i, weight=1)

        position_frame = tk.LabelFrame(self, text="현재 포지션 상세", padx=12, pady=8)
        position_frame.pack(fill="x", padx=20, pady=8)

        self.position = tk.Label(
            position_frame,
            text="방향 - / 진입가 - / 목표가 - / 손절가 - / 예상수익 -",
            anchor="w",
            font=("Malgun Gothic", 10)
        )
        self.position.pack(fill="x")

        log_frame = tk.LabelFrame(self, text="실시간 로그", padx=10, pady=8)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(8, 20))

        self.log_box = tk.Text(log_frame, height=9)
        self.log_box.pack(fill="both", expand=True)

    def _set_label_color(self, label, value):
        text = str(value).upper()
        color = "SystemButtonFace"

        if text in ["ONLINE", "실행중", "RUNNING", "실행 가능"]:
            color = "#d8f5d0"
        elif text in ["OFFLINE", "FAILED", "실행불가", "긴급정지"]:
            color = "#ffd6d6"
        elif text in ["READY", "대기", "일시정지", "정지", "설정 필요"]:
            color = "#fff1bf"

        label.config(bg=color)

    def start_run(self):
        config = load_config()
        result = run_service.start(config)

        if result.get("success"):
            state_manager.set_state("run_status", "실행중")
            add_log("실행센터: 실행 시작", "SUCCESS")
        else:
            state_manager.set_state("run_status", "실행불가")
            add_log("실행센터: 실행 실패", "ERROR")

        self.refresh()

    def pause_run(self):
        run_service.pause()
        state_manager.set_state("run_status", "일시정지")
        add_log("실행센터: 일시정지", "WARNING")
        self.refresh()

    def stop_run(self):
        run_service.stop()
        state_manager.set_state("run_status", "정지")
        add_log("실행센터: 정지", "WARNING")
        self.refresh()

    def emergency_stop(self):
        run_service.emergency_stop()
        state_manager.set_state("run_status", "긴급정지")
        add_log("실행센터: 긴급정지 실행", "ERROR")
        self.refresh()

    def refresh(self):
        config = load_config()
        status = run_service.get_runtime_status()

        project = config.get("project_name") or "-"
        strategy = config.get("strategy") or "-"
        symbol = config.get("symbol") or "-"
        api_status = state_manager.get("api_status") or "OFFLINE"

        ready = "실행 가능" if project != "-" and strategy != "-" and symbol != "-" else "설정 필요"

        info_values = {
            "project": project,
            "strategy": strategy,
            "symbol": symbol,
            "api": api_status,
            "ready": ready,
        }

        for key, value in info_values.items():
            self.info[key].config(text=value)
            self._set_label_color(self.info[key], value)

        p = int(status.get("progress", 0))
        filled = p // 10

        self.progress.config(text=f"[{'■' * filled}{'□' * (10 - filled)}] {p}%")
        self.step.config(text=f"현재 단계: {status.get('current_step', '대기')}")

        run_status = state_manager.get("run_status") or "READY"
        runtime = state_manager.get("runtime") or "00:00:00"
        current_profit = status.get("current_profit", "0.00%")
        current_position = state_manager.get("current_position") or "없음"

        status_values = {
            "run_status": run_status,
            "runtime": runtime,
            "current_profit": current_profit,
            "current_position": current_position,
        }

        for key, value in status_values.items():
            self.status_cards[key].config(text=value)
            self._set_label_color(self.status_cards[key], value)

        self.position.config(
            text=str(status.get("position") or "방향 - / 진입가 - / 목표가 - / 손절가 - / 예상수익 -")
        )

        self.log_box.delete("1.0", "end")
        logs = get_logs(50)
        self.log_box.insert("end", "\n".join(logs) if logs else "아직 로그가 없습니다.")