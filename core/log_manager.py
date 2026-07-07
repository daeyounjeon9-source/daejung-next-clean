from datetime import datetime
from pathlib import Path
from core.state_manager import state_manager
from core.event_bus import event_bus

LOG_PATH = Path(__file__).resolve().parents[1] / "data" / "logs" / "app.log"


def add_log(message, level="INFO"):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] [{level}] {message}"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    state_manager.set_state("last_log", line)
    event_bus.emit("log_added", line)
    return line


def get_logs(limit=100):
    if not LOG_PATH.exists():
        return []
    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    return lines[-limit:]


def clear_logs():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text("", encoding="utf-8")
    add_log("로그 삭제 완료", "WARNING")


def export_logs():
    return str(LOG_PATH)
