import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "config.json"
PROJECT_PATH = BASE_DIR / "config" / "project.json"

DEFAULT_CONFIG = {
    "project_name": "기본 프로젝트",
    "description": "",
    "exchange": "Binance",
    "api_key": "",
    "secret_key": "",
    "passphrase": "",
    "strategy": "EMA Cross",
    "symbol": "BTCUSDT",
    "initial_capital": "10000000",
    "amount": "10000000",
    "max_invest_ratio": "30",
    "leverage": "1",
    "max_positions": "1",
    "stop_loss": "2",
    "take_profit": "5",
    "daily_max_loss": "10",
    "auto_stop": True,
    "auto_connect": False,
    "auto_run": False,
    "auto_save": True,
}


def _read_json(path: Path):
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_config():
    # Sprint 2부터 project.json을 기준으로 사용하되, 예전 config.json도 같이 흡수한다.
    if not PROJECT_PATH.exists():
        old = _read_json(CONFIG_PATH)
        save_config({**DEFAULT_CONFIG, **old})
    data = _read_json(PROJECT_PATH)
    return {**DEFAULT_CONFIG, **data}


def save_config(config):
    PROJECT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged = {**DEFAULT_CONFIG, **config}
    with PROJECT_PATH.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    # 기존 코드 호환용으로 config.json도 같이 갱신한다.
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    return merged


def _is_number(value):
    try:
        float(str(value).replace(",", ""))
        return True
    except Exception:
        return False


def validate_config(config):
    errors = []
    required = [
        ("project_name", "프로젝트명"),
        ("exchange", "거래소"),
        ("strategy", "전략"),
        ("symbol", "종목"),
    ]
    for key, label in required:
        if not str(config.get(key, "")).strip():
            errors.append(f"{label} 값이 비어 있습니다.")

    # API는 모의 실행이 가능하도록 필수 오류가 아닌 경고 성격으로만 둔다.
    numeric = [
        ("initial_capital", "초기 투자금"),
        ("max_invest_ratio", "최대 투자 비율"),
        ("leverage", "레버리지"),
        ("max_positions", "최대 동시 포지션"),
        ("stop_loss", "손절"),
        ("take_profit", "익절"),
        ("daily_max_loss", "일 최대 손실"),
    ]
    for key, label in numeric:
        value = str(config.get(key, "")).strip()
        if value and not _is_number(value):
            errors.append(f"{label} 값은 숫자여야 합니다.")

    if _is_number(config.get("max_invest_ratio", 0)) and not (0 < float(str(config.get("max_invest_ratio")).replace(",", "")) <= 100):
        errors.append("최대 투자 비율은 1~100 사이여야 합니다.")
    if _is_number(config.get("leverage", 0)) and float(str(config.get("leverage")).replace(",", "")) <= 0:
        errors.append("레버리지는 0보다 커야 합니다.")

    return len(errors) == 0, errors


def reset_config():
    return save_config(DEFAULT_CONFIG)
