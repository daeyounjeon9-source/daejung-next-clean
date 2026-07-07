from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

@dataclass
class Order:
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    status: str = '대기'
    mode: str = 'SIMULATION'
    created_at: str = ''

class OrderManager:
    def __init__(self):
        self.orders: List[Order] = []

    def create_order(self, symbol: str, side: str, quantity: float, price: float, mode: str='SIMULATION'):
        order = Order(
            order_id=datetime.now().strftime('ORD%Y%m%d%H%M%S%f'),
            symbol=symbol,
            side=side,
            quantity=float(quantity),
            price=float(price),
            status='주문 생성',
            mode=mode,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.orders.append(order)
        return order

    def fill_order(self, order: Order):
        order.status = '체결 완료'
        return order

    def cancel_order(self, order: Order):
        order.status = '취소'
        return order

    def list_orders(self):
        return [asdict(o) for o in self.orders]

order_manager = OrderManager()
