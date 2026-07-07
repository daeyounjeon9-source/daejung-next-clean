class PortfolioManager:
    def __init__(self, initial_balance=1000000):
        self.initial_balance = float(initial_balance)
        self.balance = float(initial_balance)
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0

    def reset(self, initial_balance):
        self.initial_balance = float(initial_balance)
        self.balance = float(initial_balance)
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0

    def apply_result(self, profit_rate: float, used_amount: float):
        pnl = float(used_amount) * float(profit_rate) / 100
        self.realized_pnl += pnl
        self.balance += pnl
        return pnl

    def snapshot(self):
        today_profit_rate = 0.0
        if self.initial_balance:
            today_profit_rate = (self.balance - self.initial_balance) / self.initial_balance * 100
        return {
            'initial_balance': round(self.initial_balance, 2),
            'balance': round(self.balance, 2),
            'available_balance': round(self.balance, 2),
            'realized_pnl': round(self.realized_pnl, 2),
            'unrealized_pnl': round(self.unrealized_pnl, 2),
            'today_profit_rate': round(today_profit_rate, 2),
        }

portfolio_manager = PortfolioManager()
