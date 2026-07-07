from core.event_bus import event_bus


class StateManager:
    def __init__(self):
        self.state = {
            "current_page": "dashboard",
            "current_project": "기본",
            "exchange": "미선택",
            "api_status": "OFFLINE",
            "run_status": "READY",
            "current_strategy": "없음",
            "current_symbol": "-",
            "current_position": "없음",
            "total_asset": "0 KRW",
            "today_profit": 0.0,
            "total_profit": 0.0,
            "trade_count": 0,
            "win_rate": 0.0,
            "error_count": 0,
            "runtime": "00:00:00",
            "last_log": "",
            "config_loaded": False,
        }

    def get_state(self):
        return dict(self.state)

    def get(self, key, default=None):
        return self.state.get(key, default)

    def set_state(self, key, value):
        self.state[key] = value
        event_bus.emit("state_changed", self.get_state())

    def update_state(self, data):
        self.state.update(data)
        event_bus.emit("state_changed", self.get_state())

    def reset_state(self):
        self.__init__()
        event_bus.emit("state_changed", self.get_state())


state_manager = StateManager()
