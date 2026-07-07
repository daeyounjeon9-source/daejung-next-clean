import tkinter as tk
from tkinter import ttk, messagebox
from core.release_manager import ReleaseManager
from core.log_manager import add_log

class ReleaseCandidatePage(ttk.Frame):
    def __init__(self, master, bottom_label=None):
        super().__init__(master, padding=12)
        self.bottom_label = bottom_label
        self.manager = ReleaseManager()
        self._build()

    def _build(self):
        ttk.Label(self, text="Release Candidate 점검", font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="v03.8 단계: 배포 전 구조 점검, 안전모드 확인, 누락 파일 확인").pack(anchor="w", pady=(4, 12))

        btns = ttk.Frame(self)
        btns.pack(anchor="w", pady=8)
        ttk.Button(btns, text="RC 점검 실행", command=self.run_check).pack(side="left", padx=4)

        self.status_label = ttk.Label(self, text="상태: 대기")
        self.status_label.pack(anchor="w", pady=6)
        self.score_label = ttk.Label(self, text="점수: -")
        self.score_label.pack(anchor="w", pady=6)
        self.path_label = ttk.Label(self, text="리포트: -")
        self.path_label.pack(anchor="w", pady=6)

        columns = ("file", "description", "status")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=18)
        headers = {"file": "파일", "description": "역할", "status": "상태"}
        for col in columns:
            self.table.heading(col, text=headers[col])
            self.table.column(col, width=260 if col != "description" else 360)
        self.table.pack(fill="both", expand=True, pady=(10, 0))

    def run_check(self):
        report = self.manager.run_release_check()
        self.table.delete(*self.table.get_children())
        for item in report["items"]:
            self.table.insert("", "end", values=(item["file"], item["description"], item["status"]))
        self.status_label.config(text=f"상태: {report['status']}")
        self.score_label.config(text=f"점수: {report['score']}%")
        self.path_label.config(text=f"리포트: {report['report_path']}")
        line = add_log(f"RC 점검 완료: {report['status']} / {report['score']}%", "SUCCESS")
        if self.bottom_label:
            self.bottom_label.config(text=f"공통 로그: {line}")
        messagebox.showinfo("RC 점검", f"상태: {report['status']}\n점수: {report['score']}%")
