class RiskManager:
    """주문 전 위험 조건을 검사하는 안전장치."""
    def validate_order(self, config, signal, market_data):
        errors = []
        try:
            amount = float(config.get('amount') or 0)
        except ValueError:
            amount = 0
        try:
            leverage = float(config.get('leverage') or 1)
        except ValueError:
            leverage = 1
        try:
            stop_loss = float(config.get('stop_loss') or 0)
        except ValueError:
            stop_loss = 0
        if not signal:
            errors.append('전략 신호 없음')
        if amount <= 0:
            errors.append('투자금이 0보다 커야 함')
        if leverage <= 0 or leverage > 125:
            errors.append('레버리지는 1~125 범위 필요')
        if stop_loss <= 0:
            errors.append('손절값 필요')
        return {
            'allowed': len(errors) == 0,
            'errors': errors,
            'risk_score': min(100, int(amount * leverage / 10)) if amount else 0,
            'message': '리스크 통과' if not errors else ', '.join(errors)
        }
