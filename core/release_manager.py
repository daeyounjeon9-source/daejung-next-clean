import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "release_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CHECKS = [
    ("main.py", "프로그램 시작 파일"),
    ("ui/main_window.py", "메인 UI"),
    ("core/log_manager.py", "로그 매니저"),
    ("core/plugin_manager.py", "플러그인 매니저"),
    ("core/update_manager.py", "업데이트 매니저"),
    ("core/backtest_manager.py", "백테스트 매니저"),
    ("core/performance_monitor.py", "성능 모니터"),
    ("services/backtest_service.py", "백테스트 서비스"),
    ("services/ai_strategy_service.py", "AI 전략 보조"),
    ("services/optimization_service.py", "최적화 서비스"),
    ("config/version.json", "버전 정보"),
]

class ReleaseManager:
    def run_release_check(self):
        items = []
        ok_count = 0
        for rel, desc in CHECKS:
            path = ROOT / rel
            ok = path.exists()
            if ok:
                ok_count += 1
            items.append({
                "file": rel,
                "description": desc,
                "status": "OK" if ok else "MISSING",
            })
        version = self._load_version()
        score = round(ok_count / len(CHECKS) * 100, 1)
        status = "RC READY" if score >= 95 else "CHECK REQUIRED"
        report = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": version.get("version", "unknown"),
            "channel": version.get("channel", "unknown"),
            "score": score,
            "status": status,
            "items": items,
            "note": "실거래 주문은 기본 비활성 상태로 유지한다.",
        }
        out = REPORT_DIR / f"release_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        report["report_path"] = str(out)
        return report

    def _load_version(self):
        path = ROOT / "config" / "version.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
