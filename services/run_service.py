import json
from datetime import datetime
from pathlib import Path
from core.event_bus import event_bus
from core.log_manager import add_log
from services.api_service import api_service
from services.strategy_service import validate_strategy

RESULT_DIR = Path(__file__).resolve().parents[1] / "data" / "results"

class RunService:
    def __init__(self):
        self.runtime_status = {
            "running": False, "paused": False, "emergency": False,
            "current_step": "대기", "progress": 0, "position": None, "last_result": None,
        }

    def start(self, config):
        api_result = api_service.connect(config)
        if not api_result["success"]:
            add_log(api_result["message"], "ERROR"); return api_result
        strategy_result = validate_strategy(config)
        if not strategy_result["success"]:
            add_log(strategy_result["message"], "WARNING"); return strategy_result
        self.runtime_status.update({"running": True,"paused": False,"emergency": False,"current_step": "조건 감시 중","progress": 10})
        add_log("실행 시작", "INFO")
        event_bus.emit("run_started", self.get_runtime_status())
        return {"success": True, "message": "실행 시작"}

    def pause(self):
        self.runtime_status.update({"paused": True, "current_step": "일시정지"})
        add_log("실행 일시정지", "WARNING"); event_bus.emit("run_paused", self.get_runtime_status())

    def resume(self):
        self.runtime_status.update({"paused": False, "current_step": "조건 감시 중"})
        add_log("실행 재개", "INFO")

    def stop(self):
        self.runtime_status.update({"running": False, "paused": False, "current_step": "정지", "progress": 0})
        add_log("실행 정지", "INFO"); event_bus.emit("run_stopped", self.get_runtime_status())

    def emergency_stop(self):
        self.runtime_status.update({"running": False, "paused": False, "emergency": True, "current_step": "긴급정지", "progress": 0})
        add_log("긴급정지 실행", "ERROR"); event_bus.emit("emergency_stopped", self.get_runtime_status())

    def get_runtime_status(self):
        return dict(self.runtime_status)

    def save_result(self, result):
        RESULT_DIR.mkdir(parents=True, exist_ok=True)
        result = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), **result}
        path = RESULT_DIR / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        self.runtime_status["last_result"] = result
        event_bus.emit("result_saved", result)
        add_log("실행 결과 저장", "SUCCESS")
        return path

run_service = RunService()
