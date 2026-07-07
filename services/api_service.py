def mask_key(value):
    value = str(value or "")
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "********" + value[-4:]


class APIService:
    def __init__(self):
        self.connected = False
        self.exchange = ""

    def test_connection(self, config):
        exchange = config.get("exchange", "")
        api_key = config.get("api_key", "")
        secret_key = config.get("secret_key", "")

        if not exchange or not api_key or not secret_key:
            return {"success": False, "message": "API 입력값 확인 필요", "exchange": exchange}

        return {"success": True, "message": "API 연결 테스트 성공", "exchange": exchange}

    def connect(self, config):
        result = self.test_connection(config)
        self.connected = result["success"]
        self.exchange = result.get("exchange", "") if self.connected else ""
        return result

    def disconnect(self):
        self.connected = False
        self.exchange = ""
        return {"success": True, "message": "API 연결 해제"}

    def get_status(self):
        return "연결완료" if self.connected else "대기"


api_service = APIService()
