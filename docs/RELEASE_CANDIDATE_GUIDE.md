# DAEJUNGNEXT v03.8 Release Candidate Guide

## 목적
v03.8은 정식 릴리스 전 점검 단계입니다. 기능 추가보다 누락 파일, 안전모드, 기본 실행 흐름 확인에 집중합니다.

## 실행
```powershell
cd Desktop\DAEJUNGNEXT_V02\daejungnext_v02
python main.py
```

## 확인 순서
1. 프로그램 실행
2. RC점검 탭 이동
3. `RC 점검 실행`
4. 상태가 `RC READY`인지 확인

## 안전 원칙
- 실거래 주문은 기본 비활성입니다.
- 테스트는 모의 실행 기준입니다.
- 업데이트 전 백업 구조를 유지합니다.
