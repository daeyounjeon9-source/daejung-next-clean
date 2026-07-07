from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QProgressBar, QGroupBox, QFormLayout
from core.config_manager import load_config
from core.log_manager import get_logs
from services.run_service import run_service

class RunPage(QWidget):
    def __init__(self, result_callback=None):
        super().__init__(); self.result_callback=result_callback; self.cfg={}; self._build(); self.refresh_config()
    def _build(self):
        layout=QVBoxLayout(self)
        title=QLabel('실행센터'); title.setStyleSheet('font-size:24px;font-weight:bold;'); layout.addWidget(title)
        box=QGroupBox('현재 실행 정보'); form=QFormLayout(box); layout.addWidget(box)
        self.project=QLabel('-'); self.exchange=QLabel('-'); self.strategy=QLabel('-'); self.symbol=QLabel('-'); self.ready=QLabel('-'); self.step=QLabel('대기')
        for label,w in [('프로젝트',self.project),('거래소',self.exchange),('전략',self.strategy),('종목',self.symbol),('준비상태',self.ready),('현재단계',self.step)]: form.addRow(label,w)
        btns=QHBoxLayout(); layout.addLayout(btns)
        self.start_btn=QPushButton('모의 실행 시작'); self.pause_btn=QPushButton('일시정지'); self.resume_btn=QPushButton('재개'); self.stop_btn=QPushButton('중지'); self.emg_btn=QPushButton('긴급정지')
        for b in [self.start_btn,self.pause_btn,self.resume_btn,self.stop_btn,self.emg_btn]: btns.addWidget(b)
        self.start_btn.clicked.connect(self.start); self.pause_btn.clicked.connect(run_service.pause); self.resume_btn.clicked.connect(run_service.resume); self.stop_btn.clicked.connect(run_service.stop); self.emg_btn.clicked.connect(run_service.emergency_stop)
        self.progress=QProgressBar(); layout.addWidget(self.progress)
        self.logs=QTextEdit(); self.logs.setReadOnly(True); layout.addWidget(self.logs,1)
    def refresh_config(self):
        self.cfg=load_config(); ok,msg=run_service.check_ready(self.cfg)
        self.project.setText(self.cfg.get('project_name','-')); self.exchange.setText(self.cfg.get('exchange','-')); self.strategy.setText(self.cfg.get('strategy','-')); self.symbol.setText(self.cfg.get('symbol','-')); self.ready.setText(msg)
        self.refresh_logs()
    def start(self):
        self.refresh_config(); run_service.start_mock(self.cfg); self.refresh_logs()
    def tick(self):
        before = run_service.running
        result = run_service.tick(self.cfg)
        self.progress.setValue(run_service.progress); self.step.setText(run_service.step)
        self.refresh_logs()
        if before and result and self.result_callback: self.result_callback()
    def refresh_logs(self): self.logs.setPlainText('\n'.join(get_logs(20)))
    def is_running(self): return run_service.running
