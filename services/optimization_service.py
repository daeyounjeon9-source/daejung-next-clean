"""Safe optimization tasks for DAEJUNGNEXT.

Only removes generated cache files and empty folders. It does not delete configs,
results, reports, source code, or user-created project files.
"""
from __future__ import annotations

import shutil
import time
from pathlib import Path


class OptimizationService:
    def __init__(self, base_dir: str | Path = "."):
        self.base_dir = Path(base_dir)
        self.cache_dirs = [
            self.base_dir / "data" / "cache",
            self.base_dir / "backtest" / "cache",
        ]

    def ensure_cache_dirs(self) -> None:
        for path in self.cache_dirs:
            path.mkdir(parents=True, exist_ok=True)

    def clean_cache(self) -> dict:
        self.ensure_cache_dirs()
        removed_files = 0
        removed_dirs = 0
        for cache_dir in self.cache_dirs:
            for item in list(cache_dir.rglob("*")):
                if item.is_file():
                    try:
                        item.unlink()
                        removed_files += 1
                    except OSError:
                        pass
            for item in sorted([p for p in cache_dir.rglob("*") if p.is_dir()], reverse=True):
                try:
                    item.rmdir()
                    removed_dirs += 1
                except OSError:
                    pass
        return {
            "success": True,
            "message": "캐시 정리 완료",
            "removed_files": removed_files,
            "removed_dirs": removed_dirs,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def create_optimization_report(self) -> dict:
        reports_dir = self.base_dir / "data" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        path = reports_dir / f"optimization_report_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        content = [
            "DAEJUNGNEXT Optimization Report",
            f"Created: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "Mode: safe",
            "Actions: cache scan, generated report",
            "Note: config/results/source files are not modified.",
        ]
        path.write_text("\n".join(content), encoding="utf-8")
        return {"success": True, "path": str(path)}
