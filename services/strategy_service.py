STRATEGIES = ["스캘핑", "추세추종", "돌파매매", "평균회귀", "수동전략"]


def get_strategy_list():
    return list(STRATEGIES)


def validate_strategy(config):
    strategy = config.get("strategy", "")
    if strategy not in STRATEGIES:
        return {"success": False, "message": "전략을 선택하세요."}
    if not config.get("symbol"):
        return {"success": False, "message": "종목을 입력하세요."}
    return {"success": True, "message": "전략 검증 완료"}


def load_strategy(strategy_name):
    if strategy_name not in STRATEGIES:
        return None
    return {"name": strategy_name}


def check_entry_condition(market_data, config):
    return {"success": False, "signal": "WAIT", "message": "진입 조건 대기"}


def check_exit_condition(position_data, config):
    return {"success": False, "signal": "HOLD", "message": "청산 조건 대기"}
