class WorkflowManager:
    def __init__(self, validation_service, pipeline_service, log_manager):
        self.validation_service = validation_service
        self.pipeline_service = pipeline_service
        self.log_manager = log_manager

    def run_once(self, config):
        errors = self.validation_service.validate_before_run(config)
        if errors:
            self.log_manager.add("실행 전 점검 실패: " + ", ".join(errors), "WARNING")
            return {"success": False, "errors": errors}
        self.log_manager.add("실행 전 점검 통과", "SUCCESS")
        return self.pipeline_service.execute(config)
