class Plugin:
    def metadata(self):
        return {"name": "Scalping Strategy", "version": "0.1.0", "description": "Simple mock scalping signal"}

    def generate_signal(self, market_data):
        price = market_data.get("price", 0)
        return {"signal": "LONG" if price > 0 else "WAIT", "reason": "mock signal"}
