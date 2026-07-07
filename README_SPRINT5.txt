Sprint 5 시스템관리 센터

적용 방법:
1. 이 압축 안의 daejungnext_v02 내용을 C:\Users\user\Desktop\DAEJUNGNEXT_V02\daejungnext_v02 에 덮어쓰기
2. 터미널:
   cd "$HOME\Desktop\DAEJUNGNEXT_V02\daejungnext_v02"
   python main.py

추가/수정 파일:
- core/system_manager.py
- ui/page_5_system.py
- data/backups/
- data/exports/
- data/logs/
- data/cache/

기능:
- 시스템 상태 점검
- 전체 백업
- 설정 백업
- 로그 내보내기
- 로그 삭제
- 캐시 정리
- 환경설정 저장
