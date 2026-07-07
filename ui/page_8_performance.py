import tkinter as tk
from tkinter import ttk, messagebox

from core.log_manager import add_log
from core.performance_monitor import PerformanceMonitor
from services.optimization_service import OptimizationService


class PerformancePage(ttk.Frame):
    def __init__(self, parent, bottom_label=None):
        super().__init__(parent, padding=12)
        self.bottom_label = bottom_label
        self.monitor = PerformanceMonitor()
        self.optimizer = OptimizationService()
        self._build()
        self.refresh()

    def _build(self):
        ttk.Label(self, text="성능 최적화 센터", font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="프로그램 상태를 점검하고 안전한 캐시 정리를 실행합니다.").pack(anchor="w", pady=(2, 12))

        btns = ttk.Frame(self)
        btns.pack(anchor="w", pady=6)
        ttk.Button(btns, text="성능 점검", command=self.refresh).pack(side="left", padx=4)
        ttk.Button(btns, text="캐시 정리", command=self.clean_cache).pack(side="left", padx=4)
        ttk.Button(btns, text="최적화 리포트 저장", command=self.save_report).pack(side="left", padx=4)

        self.score_label = ttk.Label(self, text="Health Score: -", font=("Arial", 14, "bold"))
        self.score_label.pack(anchor="w", pady=(10, 4))

        columns = ("item", "value")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=14)
        self.table.heading("item", text="항목")
        self.table.heading("value", text="값")
        self.table.column("item", width=260)
        self.table.column("value", width=520)
        self.table.pack(fill="both", expand=True, pady=8)

        self.guide = tk.Text(self, height=6, wrap="word")
        self.guide.pack(fill="x", pady=(8, 0))
        self.guide.insert("1.0", "권장 순서:\n1) 성능 점검\n2) 캐시 파일이 많으면 캐시 정리\n3) 최적화 리포트 저장\n\n주의: 이 기능은 설정, 결과, 소스코드를 삭제하지 않습니다.")
        self.guide.config(state="disabled")

    def _set_bottom(self, text):
        if self.bottom_label is not None:
            self.bottom_label.config(text=f"공통 로그: {text}")

    def refresh(self):
        snap = self.monitor.snapshot()
        self.table.delete(*self.table.get_children())
        labels = {
            "timestamp": "점검 시간",
            "python_version": "Python 버전",
            "platform": "운영체제",
            "process_id": "프로세스 ID",
            "project_files": "전체 파일 수",
            "log_files": "로그 파일 수",
            "result_files": "결과/백테스트 파일 수",
            "cache_files": "캐시 파일 수",
            "estimated_project_size_kb": "예상 프로젝트 크기(KB)",
            "health_score": "상태 점수",
            "status": "판정",
        }
        for key, label in labels.items():
            self.table.insert("", "end", values=(label, snap.get(key)))
        self.score_label.config(text=f"Health Score: {snap['health_score']} / 100 ({snap['status']})")
        line = add_log(f"성능 점검 완료: {snap['health_score']}점", "INFO")
        self._set_bottom(line)

    def clean_cache(self):
        result = self.optimizer.clean_cache()
        line = add_log(f"{result['message']} / 파일 {result['removed_files']}개", "SUCCESS")
        self._set_bottom(line)
        self.refresh()
        messagebox.showinfo("캐시 정리", f"삭제 파일: {result['removed_files']}개\n삭제 폴더: {result['removed_dirs']}개")

    def save_report(self):
        result = self.optimizer.create_optimization_report()
        line = add_log("최적화 리포트 저장 완료", "SUCCESS")
        self._set_bottom(line)
        messagebox.showinfo("리포트 저장", result["path"])
