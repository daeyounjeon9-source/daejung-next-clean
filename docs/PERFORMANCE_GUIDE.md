# DAEJUNGNEXT v03.7 Performance Guide

## 목적
v03.7은 실행 안정화를 위해 성능 점검과 안전한 캐시 정리 기능을 추가합니다.

## 포함 기능
- 프로젝트 파일 수 점검
- 로그/결과/캐시 파일 수 점검
- Health Score 산출
- 안전 캐시 정리
- 최적화 리포트 저장

## 안전 원칙
캐시 정리는 `data/cache`, `backtest/cache`만 대상으로 하며 설정, 결과, 소스코드는 삭제하지 않습니다.
