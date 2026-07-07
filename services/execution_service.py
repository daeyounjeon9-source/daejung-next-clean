from core.order_manager import order_manager
from core.position_manager import position_manager

class ExecutionService:
    def submit_simulation_order(self, symbol, side, quantity, price):
        order = order_manager.create_order(symbol, side, quantity, price, mode='SIMULATION')
        order_manager.fill_order(order)
        position_manager.open_position(symbol, side, price, quantity)
        return order

execution_service = ExecutionService()
