from core.portfolio_manager import portfolio_manager

class AccountService:
    def load_from_config(self, config):
        try:
            amount = float(str(config.get('initial_amount', '1000000')).replace(',', ''))
        except Exception:
            amount = 1000000
        portfolio_manager.reset(amount)
        return portfolio_manager.snapshot()

    def get_account(self):
        return portfolio_manager.snapshot()

account_service = AccountService()
