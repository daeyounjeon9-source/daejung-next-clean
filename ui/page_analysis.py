from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from core.result_manager import load_results

class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__(); self._build(); self.refresh()
    def _build(self):
        layout=QVBoxLayout(self); title=QLabel('결과분석'); title.setStyleSheet('font-size:24px;font-weight:bold;'); layout.addWidget(title)
        self.summary=QLabel('총 거래 0 / 승률 0.0% / 누적손익 0.00%'); layout.addWidget(self.summary)
        b=QPushButton('새로고침'); b.clicked.connect(self.refresh); layout.addWidget(b)
        self.table=QTableWidget(0,7); self.table.setHorizontalHeaderLabels(['시간','프로젝트','거래소','전략','종목','방향','수익률']); layout.addWidget(self.table,1)
    def refresh(self):
        rows=load_results(); profits=[float(r.get('profit_rate',0)) for r in rows]; wins=sum(1 for p in profits if p>=0); total=len(rows)
        self.summary.setText(f'총 거래 {total} / 승률 {(wins/total*100 if total else 0):.1f}% / 누적손익 {sum(profits):+.2f}%')
        self.table.setRowCount(total)
        for i,r in enumerate(rows):
            vals=[r.get('time',''),r.get('project_name',''),r.get('exchange',''),r.get('strategy',''),r.get('symbol',''),r.get('side',''),str(r.get('profit_rate',''))]
            for j,v in enumerate(vals): self.table.setItem(i,j,QTableWidgetItem(v))
