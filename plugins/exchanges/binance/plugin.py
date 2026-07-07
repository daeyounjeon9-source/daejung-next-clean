class Plugin:
    def metadata(self):
        return {"name": "Binance Exchange", "version": "0.1.0", "description": "Binance API adapter placeholder"}

    def test_connection(self, config=None):
        return {"success": True, "message": "Binance mock connection OK", "latency_ms": 18}
