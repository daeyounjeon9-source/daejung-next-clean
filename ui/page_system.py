from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from core.log_manager import get_logs

class SystemPage(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self); title=QLabel('시스템관리'); title.setStyleSheet('font-size:24px;font-weight:bold;'); layout.addWidget(title)
        layout.addWidget(QLabel('대정NEXT 시스템 상태: 정상 / 안전모드 / 실거래 비활성'))
        b=QPushButton('로그 새로고침'); layout.addWidget(b); self.logs=QTextEdit(); self.logs.setReadOnly(True); layout.addWidget(self.logs,1); b.clicked.connect(self.refresh); self.refresh()
    def refresh(self): self.logs.setPlainText('\n'.join(get_logs(100)))
