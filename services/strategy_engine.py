class StrategyEngine:
    """전략 조건 계산 엔진. v02.8에서는 모의 신호만 생성."""
    def evaluate(self, market_series, config):
        if len(market_series) < 2:
            return {'signal': None, 'reason': '시장 데이터 부족', 'confidence': 0}
        first = market_series[0]['price']
        last = market_series[-1]['price']
        change = (last - first) / first * 100
        strategy = config.get('strategy', '스캘핑')
        if strategy == '추세추종':
            signal = 'LONG' if change >= 0 else 'SHORT'
        elif strategy == '평균회귀':
            signal = 'SHORT' if change >= 0.3 else 'LONG'
        elif strategy == '돌파매매':
            signal = 'LONG' if change >= 0.15 else None
        elif strategy == '수동전략':
            signal = None
        else:
            signal = 'LONG' if change >= -0.1 else 'SHORT'
        return {
            'signal': signal,
            'reason': f'{strategy} 기준 변화율 {round(change, 3)}%',
            'confidence': min(95, max(10, int(abs(change) * 100) + 45)),
            'change_rate': round(change, 3)
        }
