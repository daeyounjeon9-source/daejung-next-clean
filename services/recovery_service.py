class RecoveryService:
    def __init__(self, log_manager):
        self.log_manager = log_manager

    def recover_runtime(self):
        self.log_manager.add("Runtime 복구 점검 완료", "INFO")
        return True

    def reconnect_api(self):
        self.log_manager.add("API 재연결 시도 완료(모의)", "INFO")
        return True
