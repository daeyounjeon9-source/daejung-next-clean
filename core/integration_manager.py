from core.state_manager import StateManager
from core.config_manager import ConfigManager
from core.log_manager import LogManager
from core.event_bus import EventBus
from core.result_manager import ResultManager
from core.health_monitor import HealthMonitor
from core.workflow_manager import WorkflowManager
from services.validation_service import ValidationService
from services.pipeline_service import PipelineService
from services.recovery_service import RecoveryService

class IntegrationManager:
    def __init__(self):
        self.state = StateManager()
        self.config = ConfigManager()
        self.log = LogManager()
        self.event = EventBus()
        self.results = ResultManager()
        self.health = HealthMonitor()
        self.validation = ValidationService()
        self.pipeline = PipelineService(self.results, self.log)
        self.recovery = RecoveryService(self.log)
        self.workflow = WorkflowManager(self.validation, self.pipeline, self.log)
        self.current_config = None

    def initialize(self):
        self.current_config = self.config.load()
        self.state.update({
            "current_project": self.current_config.get("project_name", ""),
            "run_status": "준비",
            "api_status": "모의연결",
        })
        self.log.add("통합 엔진 초기화 완료", "SUCCESS")

    def run_pipeline_once(self):
        result = self.workflow.run_once(self.current_config)
        if result.get("success"):
            self.state.update({"run_status": "완료", "trade_count": self.state.get("trade_count") + 1})
        else:
            self.state.update({"run_status": "점검필요", "error_count": self.state.get("error_count") + 1})
        return result

    def check_health(self):
        health = self.health.check(self.state.get())
        self.state.set("health", health["status"])
        return health
