from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Position:
    symbol: str
    side: str
    entry_price: float
    quantity: float
    current_price: float
    opened_at: str

    @property
    def pnl_rate(self):
        if self.entry_price == 0:
            return 0.0
        if self.side == 'LONG':
            return (self.current_price - self.entry_price) / self.entry_price * 100
        return (self.entry_price - self.current_price) / self.entry_price * 100

class PositionManager:
    def __init__(self):
        self.position: Optional[Position] = None

    def open_position(self, symbol: str, side: str, entry_price: float, quantity: float):
        self.position = Position(symbol, side, float(entry_price), float(quantity), float(entry_price), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return self.position

    def update_price(self, price: float):
        if self.position:
            self.position.current_price = float(price)
        return self.position

    def close_position(self, exit_price: float):
        if not self.position:
            return None
        self.position.current_price = float(exit_price)
        closed = asdict(self.position)
        closed['exit_price'] = float(exit_price)
        closed['profit_rate'] = round(self.position.pnl_rate, 2)
        self.position = None
        return closed

    def snapshot(self):
        if not self.position:
            return None
        data = asdict(self.position)
        data['profit_rate'] = round(self.position.pnl_rate, 2)
        return data

position_manager = PositionManager()
