from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame
from core.config_manager import load_config
from core.result_manager import load_results

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__(); self.cards={}; self._build(); self.refresh()
    def _build(self):
        layout=QVBoxLayout(self); title=QLabel('메인 대시보드'); title.setStyleSheet('font-size:24px;font-weight:bold;'); layout.addWidget(title)
        grid=QGridLayout(); layout.addLayout(grid)
        names=['프로젝트','거래소','전략','현재 종목','오늘 손익','거래횟수','승률','실행상태']
        for i,n in enumerate(names):
            box=QFrame(); box.setStyleSheet('background:white;border:1px solid #ddd;border-radius:8px;padding:12px;')
            bl=QVBoxLayout(box); bl.addWidget(QLabel(n)); val=QLabel('-'); val.setStyleSheet('font-size:20px;font-weight:bold;'); bl.addWidget(val)
            self.cards[n]=val; grid.addWidget(box,i//4,i%4)
        self.memo=QLabel('운영 메모: 입력센터에서 설정 저장 후 실행센터에서 모의 실행을 시작하세요.'); layout.addWidget(self.memo); layout.addStretch()
    def refresh(self):
        cfg=load_config(); results=load_results()
        profits=[float(r.get('profit_rate',0)) for r in results]
        wins=sum(1 for p in profits if p>=0); total=len(profits)
        self.cards['프로젝트'].setText(cfg.get('project_name','-'))
        self.cards['거래소'].setText(cfg.get('exchange','-'))
        self.cards['전략'].setText(cfg.get('strategy','-'))
        self.cards['현재 종목'].setText(cfg.get('symbol','-'))
        self.cards['오늘 손익'].setText(f"{sum(profits):+.2f}%")
        self.cards['거래횟수'].setText(str(total))
        self.cards['승률'].setText(f"{(wins/total*100 if total else 0):.1f}%")
        self.cards['실행상태'].setText('READY')
