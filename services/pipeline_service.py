from datetime import datetime
import random

class PipelineService:
    def __init__(self, result_manager, log_manager):
        self.result_manager = result_manager
        self.log_manager = log_manager

    def execute(self, config):
        self.log_manager.add("파이프라인 시작", "INFO")
        signal = random.choice(["LONG", "SHORT", "WAIT"])
        profit = 0.0 if signal == "WAIT" else round(random.uniform(-1.2, 2.4), 2)
        result = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_name": config.get("project_name"),
            "exchange": config.get("exchange"),
            "strategy": config.get("strategy"),
            "symbol": config.get("symbol"),
            "side": signal,
            "entry_price": 65000,
            "exit_price": round(65000 * (1 + profit / 100), 2),
            "profit_rate": profit,
            "result": "대기" if signal == "WAIT" else ("성공" if profit >= 0 else "실패"),
            "mode": "simulation"
        }
        path = self.result_manager.save_result(result)
        self.log_manager.add(f"결과 저장 완료: {path}", "SUCCESS")
        return {"success": True, "result": result, "path": path}
