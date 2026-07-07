class Plugin:
    def metadata(self):
        return {"name": "RSI Indicator", "version": "0.1.0", "description": "RSI indicator placeholder"}

    def calculate(self, values):
        return 50.0
