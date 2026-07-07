import tkinter as tk
from datetime import datetime

from core.event_bus import event_bus
from core.log_manager import add_log
from core.state_manager import state_manager
from ui.page_1_dashboard import DashboardPage
from ui.page_2_input import InputPage
from ui.page_3_run import RunPage
from ui.page_4_analysis import AnalysisPage
from ui.page_5_system import SystemPage


PAGE_LABELS = {
    "dashboard": "1 메인",
    "input": "2 입력센터",
    "run": "3 실행센터",
    "analysis": "4 결과분석",
    "system": "5 시스템관리",
}


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("대정NEXT - Sprint 2 입력센터")
        self.root.geometry("1180x760")
        self.root.minsize(1040, 680)

        self.current_page = None
        self.pages = {}
        self.menu_buttons = {}

        self._build_layout()
        self._bind_events()
        self.show_page("dashboard")
        self._tick_clock()

    def _build_layout(self):
        self.top_bar = tk.Frame(self.root, height=44, bd=1, relief="solid")
        self.top_bar.pack(side="top", fill="x")

        self.title_label = tk.Label(self.top_bar, text="대정NEXT", font=("Malgun Gothic", 14, "bold"), width=16, anchor="w")
        self.title_label.pack(side="left", padx=12)
        self.page_label = tk.Label(self.top_bar, text="현재 페이지", font=("Malgun Gothic", 11), width=18, anchor="w")
        self.page_label.pack(side="left")
        self.project_label = tk.Label(self.top_bar, text="프로젝트: 기본", width=20, anchor="w")
        self.project_label.pack(side="left")
        self.api_label = tk.Label(self.top_bar, text="API: OFFLINE", width=16, anchor="w")
        self.api_label.pack(side="left")
        self.run_label = tk.Label(self.top_bar, text="실행: READY", width=16, anchor="w")
        self.strategy_label = tk.Label(self.top_bar, text="전략: 없음", width=16, anchor="w")
        self.run_label.pack(side="left")
        self.strategy_label.pack(side="left")
        self.clock_label = tk.Label(self.top_bar, text="", anchor="e")
        self.clock_label.pack(side="right", padx=12)

        self.body = tk.Frame(self.root)
        self.body.pack(side="top", fill="both", expand=True)

        self.side_menu = tk.Frame(self.body, width=160, bd=1, relief="solid")
        self.side_menu.pack(side="left", fill="y")
        self.side_menu.pack_propagate(False)

        tk.Label(self.side_menu, text="메뉴", font=("Malgun Gothic", 12, "bold")).pack(fill="x", pady=(14, 8))
        for key, label in PAGE_LABELS.items():
            btn = tk.Button(self.side_menu, text=label, height=2, command=lambda k=key: self.show_page(k))
            btn.pack(fill="x", padx=10, pady=4)
            self.menu_buttons[key] = btn

        self.content_area = tk.Frame(self.body, bd=1, relief="solid")
        self.content_area.pack(side="left", fill="both", expand=True)

        self.bottom_log = tk.Label(self.root, text="공통 로그: 준비 | Python OK | 프로젝트: 기본 | 버전: Sprint 2", anchor="w", height=2, bd=1, relief="solid")
        self.bottom_log.pack(side="bottom", fill="x")

    def _bind_events(self):
        event_bus.subscribe("log_added", self._on_log_added)
        event_bus.subscribe("state_changed", self._on_state_changed)
        event_bus.subscribe("config_saved", lambda data: self._refresh_all_pages())
        event_bus.subscribe("run_started", lambda data: self._refresh_all_pages())
        event_bus.subscribe("run_stopped", lambda data: self._refresh_all_pages())
        event_bus.subscribe("emergency_stopped", lambda data: self._refresh_all_pages())
        event_bus.subscribe("result_saved", lambda data: self._refresh_all_pages())

    def _make_page(self, page_name):
        classes = {
            "dashboard": DashboardPage,
            "input": InputPage,
            "run": RunPage,
            "analysis": AnalysisPage,
            "system": SystemPage,
        }
        return classes[page_name](self.content_area)

    def show_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].pack_forget()

        if page_name not in self.pages:
            self.pages[page_name] = self._make_page(page_name)

        self.current_page = page_name
        self.pages[page_name].pack(fill="both", expand=True)
        self.pages[page_name].refresh()
        state_manager.set_state("current_page", page_name)
        self.page_label.config(text=PAGE_LABELS.get(page_name, page_name))

        for key, btn in self.menu_buttons.items():
            btn.config(relief="sunken" if key == page_name else "raised")
        add_log(f"페이지 이동: {PAGE_LABELS.get(page_name, page_name)}", "INFO")

    def _refresh_all_pages(self):
        for page in self.pages.values():
            page.refresh()
        self._on_state_changed(state_manager.get_state())

    def _on_log_added(self, line):
        self.bottom_log.config(text=f"공통 로그: {line}")

    def _on_state_changed(self, data):
        self.project_label.config(text=f"프로젝트: {state_manager.get('current_project', '기본')}")
        self.api_label.config(text=f"API: {state_manager.get('api_status', 'OFFLINE')}")
        self.run_label.config(text=f"실행: {state_manager.get('run_status', 'READY')}")
        self.strategy_label.config(text=f"전략: {state_manager.get('current_strategy', '없음')}")

    def _tick_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def run(self):
        add_log("대정NEXT 프로그램 시작", "INFO")
        self.root.mainloop()
