from datetime import datetime

class HealthMonitor:
    def __init__(self):
        self.last_check = None
        self.status = "정상"
        self.last_error = ""

    def check(self, state):
        self.last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if state.get("api_status") == "오류":
            self.status = "주의"
            self.last_error = "API 상태 오류"
        else:
            self.status = "정상"
            self.last_error = ""
        return {"status": self.status, "last_check": self.last_check, "last_error": self.last_error}
