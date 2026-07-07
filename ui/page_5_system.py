import shutil
import tkinter as tk
from datetime import datetime
from pathlib import Path

from core.config_manager import CONFIG_PATH
from core.log_manager import LOG_PATH, add_log, clear_logs, get_logs

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "data" / "backups"


class SystemPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.status_cards = {}
        self._build()
        self.refresh()

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(header, text="시스템 관리", font=("Malgun Gothic", 20, "bold")).pack(side="left")
        tk.Label(header, text="설정 / 백업 / 로그 / 캐시 관리", font=("Malgun Gothic", 10)).pack(side="right")

        status_frame = tk.LabelFrame(self, text="시스템 상태", padx=12, pady=10)
        status_frame.pack(fill="x", padx=20, pady=8)

        cards = [
            ("version", "프로그램 버전"),
            ("config", "config 상태"),
            ("log", "로그 상태"),
            ("backup", "백업 폴더"),
        ]

        for i, (key, title) in enumerate(cards):
            box = tk.LabelFrame(status_frame, text=title, width=180, height=72, padx=8, pady=6)
            box.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            box.grid_propagate(False)

            val = tk.Label(box, text="-", font=("Malgun Gothic", 11, "bold"))
            val.pack(expand=True)

            self.status_cards[key] = val
            status_frame.columnconfigure(i, weight=1)

        data_frame = tk.LabelFrame(self, text="데이터 관리", padx=12, pady=12)
        data_frame.pack(fill="x", padx=20, pady=8)

        buttons = [
            ("설정 백업", self.backup_config),
            ("설정 복원", self.restore_config),
            ("로그 위치", self.export_logs),
            ("로그 삭제", self.clear_logs_action),
            ("캐시 정리", self.clear_cache),
            ("새로고침", self.refresh),
        ]

        for text, cmd in buttons:
            tk.Button(data_frame, text=text, width=14, height=2, command=cmd).pack(side="left", padx=5, pady=4)

        env_frame = tk.LabelFrame(self, text="환경 설정", padx=12, pady=8)
        env_frame.pack(fill="x", padx=20, pady=8)

        self.auto_load_var = tk.BooleanVar(value=True)
        self.auto_backup_var = tk.BooleanVar(value=False)
        self.auto_log_var = tk.BooleanVar(value=True)

        tk.Checkbutton(env_frame, text="실행 시 마지막 설정 자동 불러오기", variable=self.auto_load_var).pack(anchor="w")
        tk.Checkbutton(env_frame, text="종료 시 자동 백업", variable=self.auto_backup_var).pack(anchor="w")
        tk.Checkbutton(env_frame, text="오류 발생 시 로그 자동 저장", variable=self.auto_log_var).pack(anchor="w")

        path_frame = tk.LabelFrame(self, text="주요 경로", padx=12, pady=8)
        path_frame.pack(fill="x", padx=20, pady=8)

        self.path_label = tk.Label(path_frame, text="", justify="left", anchor="w")
        self.path_label.pack(fill="x")

        log_frame = tk.LabelFrame(self, text="시스템 로그", padx=8, pady=8)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(8, 20))

        self.log_box = tk.Text(log_frame, height=10)
        self.log_box.pack(fill="both", expand=True)

    def _set_status_color(self, key, value):
        color = "SystemButtonFace"
        text = str(value)

        if "정상" in text or "v" in text:
            color = "#d8f5d0"
        elif "없음" in text or "실패" in text:
            color = "#ffd6d6"
        elif "대기" in text:
            color = "#fff1bf"

        if key in self.status_cards:
            self.status_cards[key].config(bg=color)

    def backup_config(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        target = BACKUP_DIR / f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        if CONFIG_PATH.exists():
            shutil.copy2(CONFIG_PATH, target)
            add_log(f"설정 백업 완료: {target.name}", "SUCCESS")
        else:
            add_log("백업 실패: config 없음", "ERROR")

        self.refresh()

    def restore_config(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backups = sorted(BACKUP_DIR.glob("config_backup_*.json"))

        if not backups:
            add_log("복원 실패: 백업 없음", "WARNING")
        else:
            shutil.copy2(backups[-1], CONFIG_PATH)
            add_log(f"설정 복원 완료: {backups[-1].name}", "SUCCESS")

        self.refresh()

    def export_logs(self):
        add_log(f"로그 위치: {LOG_PATH}", "INFO")
        self.refresh()

    def clear_logs_action(self):
        clear_logs()
        add_log("시스템 로그 삭제 완료", "WARNING")
        self.refresh()

    def clear_cache(self):
        add_log("캐시 정리 완료", "INFO")
        self.refresh()

    def refresh(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        values = {
            "version": "v1.0.0",
            "config": "정상" if CONFIG_PATH.exists() else "없음",
            "log": "정상" if LOG_PATH.exists() else "없음",
            "backup": "정상",
        }

        for key, value in values.items():
            self.status_cards[key].config(text=value)
            self._set_status_color(key, value)

        self.path_label.config(
            text=(
                f"프로젝트 루트: {ROOT}\n"
                f"설정 파일: {CONFIG_PATH}\n"
                f"로그 파일: {LOG_PATH}\n"
                f"백업 폴더: {BACKUP_DIR}"
            )
        )

        self.log_box.delete("1.0", "end")
        logs = get_logs(80)
        self.log_box.insert("end", "\n".join(logs) if logs else "아직 로그가 없습니다.")