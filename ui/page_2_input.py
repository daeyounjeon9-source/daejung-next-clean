import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from core.config_manager import load_config, save_config, validate_config, reset_config, PROJECT_PATH
from core.event_bus import event_bus
from core.log_manager import add_log
from core.state_manager import state_manager
from services.api_service import api_service


EXCHANGES = ["Binance", "Bybit", "Upbit", "Bithumb"]
STRATEGIES = ["EMA Cross", "RSI", "MACD", "Custom Strategy"]


class InputPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.entries = {}
        self.vars = {}
        self._build()
        self.load_config()

    def _entry(self, parent, key, label, show=None, width=28):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, width=16, anchor="w").pack(side="left")
        ent = tk.Entry(row, show=show, width=width)
        ent.pack(side="left", fill="x", expand=True)
        self.entries[key] = ent
        ent.bind("<KeyRelease>", lambda _e: self.refresh())
        return ent

    def _option(self, parent, key, label, values):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, width=16, anchor="w").pack(side="left")
        var = tk.StringVar(value=values[0])
        menu = tk.OptionMenu(row, var, *values, command=lambda _v: self.refresh())
        menu.pack(side="left", fill="x", expand=True)
        self.vars[key] = var
        return var

    def _check(self, parent, key, label):
        var = tk.BooleanVar(value=False)
        tk.Checkbutton(parent, text=label, variable=var, command=self.refresh).pack(anchor="w", pady=2)
        self.vars[key] = var
        return var

    def _build(self):
        tk.Label(self, text="입력센터", font=("Malgun Gothic", 18, "bold"), anchor="w").pack(fill="x", padx=20, pady=(14, 8))
        tk.Label(self, text="프로젝트 / 거래소 / API / 거래조건 / 전략 / 리스크를 저장합니다.", anchor="w").pack(fill="x", padx=20)

        wrap = tk.Frame(self)
        wrap.pack(fill="both", expand=True, padx=20, pady=10)

        left = tk.Frame(wrap)
        left.pack(side="left", fill="both", expand=True)
        mid = tk.Frame(wrap)
        mid.pack(side="left", fill="both", expand=True, padx=(14, 0))
        right = tk.LabelFrame(wrap, text="저장 상태", width=280, padx=12, pady=12)
        right.pack(side="right", fill="y", padx=(14, 0))
        right.pack_propagate(False)

        self.status_label = tk.Label(right, text="대기", justify="left", anchor="nw")
        self.status_label.pack(fill="both", expand=True)

        project = tk.LabelFrame(left, text="① 프로젝트 정보", padx=12, pady=8)
        project.pack(fill="x", pady=6)
        self._entry(project, "project_name", "프로젝트명")
        self._entry(project, "description", "프로젝트 설명")

        exchange = tk.LabelFrame(left, text="② 거래소 설정", padx=12, pady=8)
        exchange.pack(fill="x", pady=6)
        self._option(exchange, "exchange", "거래소", EXCHANGES)

        api = tk.LabelFrame(left, text="③ API 설정", padx=12, pady=8)
        api.pack(fill="x", pady=6)
        self._entry(api, "api_key", "API Key")
        self._entry(api, "secret_key", "Secret Key", show="*")
        self._entry(api, "passphrase", "Passphrase", show="*")
        tk.Button(api, text="연결 테스트", command=self.test_api_connection).pack(anchor="e", pady=4)

        trade = tk.LabelFrame(mid, text="④ 거래 설정", padx=12, pady=8)
        trade.pack(fill="x", pady=6)
        self._entry(trade, "initial_capital", "초기 투자금")
        self._entry(trade, "max_invest_ratio", "최대 투자 비율(%)")
        self._entry(trade, "leverage", "레버리지(x)")
        self._entry(trade, "max_positions", "최대 동시 포지션")
        self._entry(trade, "symbol", "기본 종목")

        strategy = tk.LabelFrame(mid, text="⑤ 전략 설정", padx=12, pady=8)
        strategy.pack(fill="x", pady=6)
        self._option(strategy, "strategy", "전략", STRATEGIES)

        risk = tk.LabelFrame(mid, text="⑥ 리스크 관리", padx=12, pady=8)
        risk.pack(fill="x", pady=6)
        self._entry(risk, "stop_loss", "손절(%)")
        self._entry(risk, "take_profit", "익절(%)")
        self._entry(risk, "daily_max_loss", "일 최대 손실(%)")
        self._check(risk, "auto_stop", "일 최대 손실 초과 시 자동 중지")
        self._check(risk, "auto_connect", "시작 시 자동 연결")
        self._check(risk, "auto_run", "조건 충족 시 자동 실행")
        self._check(risk, "auto_save", "종료 시 자동 저장")

        btns = tk.Frame(self)
        btns.pack(fill="x", padx=20, pady=(0, 14))
        for text, cmd in [("초기화", self.reset_form), ("불러오기", self.load_config), ("저장", self.save_config), ("적용", self.apply_config)]:
            tk.Button(btns, text=text, width=14, height=2, command=cmd).pack(side="left", padx=5)

    def collect(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        for key, var in self.vars.items():
            data[key] = var.get()
        # 기존 서비스 호환용
        data["amount"] = data.get("initial_capital", "")
        return data

    def fill(self, config):
        for key, ent in self.entries.items():
            ent.delete(0, "end")
            ent.insert(0, str(config.get(key, "")))
        for key, var in self.vars.items():
            if isinstance(var, tk.BooleanVar):
                var.set(bool(config.get(key, False)))
            else:
                var.set(str(config.get(key, var.get()) or var.get()))
        self.refresh()

    def load_config(self):
        self.fill(load_config())
        add_log("입력센터: 설정 불러오기 완료", "INFO")

    def save_config(self):
        config = self.collect()
        ok, errors = validate_config(config)
        if not ok:
            self.refresh(errors)
            messagebox.showwarning("입력 확인", "\n".join(errors))
            add_log(f"입력센터: 설정 저장 실패({len(errors)}개 오류)", "WARNING")
            return False

        saved = save_config(config)
        state_manager.update_state({
            "current_project": saved.get("project_name", "기본"),
            "exchange": saved.get("exchange", "미선택"),
            "current_strategy": saved.get("strategy", "없음"),
            "current_symbol": saved.get("symbol", "-"),
            "total_asset": f"{saved.get('initial_capital', '0')} KRW",
            "config_loaded": True,
        })
        add_log("입력센터: project.json 저장 완료", "SUCCESS")
        event_bus.emit("config_saved", saved)
        self.refresh([])
        return True

    def apply_config(self):
        if self.save_config():
            add_log("입력센터: 설정 적용 완료", "SUCCESS")
            messagebox.showinfo("적용 완료", "설정이 저장되고 대시보드에 반영되었습니다.")

    def test_api_connection(self):
        result = api_service.test_connection(self.collect())
        state_manager.set_state("api_status", "ONLINE" if result.get("success") else "FAILED")
        add_log(result.get("message", "API 테스트 완료"), "SUCCESS" if result.get("success") else "ERROR")
        event_bus.emit("api_test_success" if result.get("success") else "api_test_failed", result)
        self.refresh()

    def reset_form(self):
        if messagebox.askyesno("초기화", "입력값을 기본값으로 초기화할까요?"):
            self.fill(reset_config())
            add_log("입력센터: 입력값 초기화 완료", "WARNING")

    def refresh(self, errors=None):
        try:
            config = self.collect()
        except Exception:
            config = load_config()
        if errors is None:
            _, errors = validate_config(config)
        important_keys = [
            "project_name", "exchange", "strategy", "symbol", "initial_capital",
            "max_invest_ratio", "leverage", "max_positions", "stop_loss", "take_profit", "daily_max_loss",
        ]
        filled = sum(1 for k in important_keys if str(config.get(k, "")).strip())
        rate = int(filled / len(important_keys) * 100)
        api_mask = "입력됨" if config.get("api_key") else "미입력"
        secret_mask = "입력됨" if config.get("secret_key") else "미입력"
        saved_text = "저장됨" if state_manager.get("config_loaded") else "대기"
        self.status_label.config(text=(
            f"저장 상태: {saved_text}\n"
            f"저장 파일: config/project.json\n"
            f"프로젝트: {config.get('project_name') or '-'}\n"
            f"거래소: {config.get('exchange') or '-'}\n"
            f"전략: {config.get('strategy') or '-'}\n"
            f"종목: {config.get('symbol') or '-'}\n"
            f"API Key: {api_mask}\n"
            f"Secret: {secret_mask}\n"
            f"입력 완료율: {rate}%\n"
            f"오류 개수: {len(errors)}\n"
            f"마지막 확인: {datetime.now().strftime('%H:%M:%S')}\n"
            f"경로:\n{PROJECT_PATH}"
        ))
