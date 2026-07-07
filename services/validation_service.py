class ValidationService:
    def validate_before_run(self, config):
        errors = []
        if config.get("mode") != "simulation":
            errors.append("현재 버전은 simulation 모드만 허용됩니다")
        try:
            amount = float(config.get("amount", 0))
            if amount <= 0:
                errors.append("투자금은 0보다 커야 합니다")
        except Exception:
            errors.append("투자금 숫자 형식 오류")
        if not config.get("symbol"):
            errors.append("종목이 없습니다")
        return errors
