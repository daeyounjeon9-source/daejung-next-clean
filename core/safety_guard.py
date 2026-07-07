SIMULATION_MODE = True
LIVE_TRADING_ENABLED = False

def assert_safe_to_trade(live_requested: bool = False):
    if live_requested and not LIVE_TRADING_ENABLED:
        return False, "실거래는 비활성 상태입니다. 현재는 모의 실행만 허용됩니다."
    return True, "안전 모드 확인 완료"

def mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "*" * (len(value) - 8) + value[-4:]
