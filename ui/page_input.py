from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QHBoxLayout, QMessageBox
from core.config_manager import load_config, save_config, reset_config
from core.log_manager import add_log

class InputPage(QWidget):
    def __init__(self, saved_callback=None):
        super().__init__(); self.saved_callback=saved_callback; self._build(); self.load()
    def _build(self):
        layout=QVBoxLayout(self); form=QFormLayout(); layout.addLayout(form)
        self.project=QLineEdit(); self.desc=QLineEdit(); self.exchange=QComboBox(); self.exchange.addItems(['Binance','Bybit','Upbit','Bithumb'])
        self.api=QLineEdit(); self.secret=QLineEdit(); self.secret.setEchoMode(QLineEdit.Password); self.passphrase=QLineEdit(); self.passphrase.setEchoMode(QLineEdit.Password)
        self.symbol=QLineEdit(); self.amount=QLineEdit(); self.ratio=QLineEdit(); self.leverage=QLineEdit(); self.maxpos=QLineEdit()
        self.strategy=QComboBox(); self.strategy.addItems(['EMA Cross','RSI','MACD','Custom Strategy'])
        self.sl=QLineEdit(); self.tp=QLineEdit(); self.daily=QLineEdit(); self.autostop=QCheckBox('자동 중지 ON')
        for label, w in [('프로젝트명',self.project),('설명',self.desc),('거래소',self.exchange),('API Key',self.api),('Secret Key',self.secret),('Passphrase',self.passphrase),('종목',self.symbol),('초기 투자금',self.amount),('최대 투자 비율(%)',self.ratio),('레버리지',self.leverage),('최대 동시 포지션',self.maxpos),('전략',self.strategy),('손절(%)',self.sl),('익절(%)',self.tp),('일 최대 손실(%)',self.daily),('자동 중지',self.autostop)]: form.addRow(label,w)
        row=QHBoxLayout(); layout.addLayout(row)
        for text, fn in [('저장',self.save),('불러오기',self.load),('초기화',self.reset)]:
            b=QPushButton(text); b.clicked.connect(fn); row.addWidget(b)
        layout.addStretch()
    def get_data(self):
        return {'project_name':self.project.text(),'description':self.desc.text(),'exchange':self.exchange.currentText(),'api_key':self.api.text(),'secret_key':self.secret.text(),'passphrase':self.passphrase.text(),'symbol':self.symbol.text(),'initial_amount':self.amount.text(),'max_ratio':self.ratio.text(),'leverage':self.leverage.text(),'max_positions':self.maxpos.text(),'strategy':self.strategy.currentText(),'stop_loss':self.sl.text(),'take_profit':self.tp.text(),'daily_loss_limit':self.daily.text(),'auto_stop':self.autostop.isChecked()}
    def set_data(self,c):
        self.project.setText(c.get('project_name','')); self.desc.setText(c.get('description','')); self.exchange.setCurrentText(c.get('exchange','Binance')); self.api.setText(c.get('api_key','')); self.secret.setText(c.get('secret_key','')); self.passphrase.setText(c.get('passphrase','')); self.symbol.setText(c.get('symbol','')); self.amount.setText(c.get('initial_amount','')); self.ratio.setText(c.get('max_ratio','')); self.leverage.setText(c.get('leverage','')); self.maxpos.setText(c.get('max_positions','')); self.strategy.setCurrentText(c.get('strategy','EMA Cross')); self.sl.setText(c.get('stop_loss','')); self.tp.setText(c.get('take_profit','')); self.daily.setText(c.get('daily_loss_limit','')); self.autostop.setChecked(bool(c.get('auto_stop',True)))
    def save(self):
        save_config(self.get_data()); add_log('입력센터 설정 저장 완료','SUCCESS'); QMessageBox.information(self,'저장','설정 저장 완료')
        if self.saved_callback: self.saved_callback()
    def load(self): self.set_data(load_config()); add_log('입력센터 설정 불러오기','INFO')
    def reset(self): self.set_data(reset_config()); add_log('입력센터 초기화','WARNING')
