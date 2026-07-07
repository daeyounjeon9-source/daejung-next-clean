"""DAEJUNGNEXT performance monitoring helpers.

This module avoids third-party dependencies so it can run on a clean Python install.
It reads lightweight runtime metrics and returns them in a UI-friendly format.
"""
from __future__ import annotations

import os
import platform
import time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PerformanceSnapshot:
    timestamp: str
    python_version: str
    platform: str
    process_id: int
    project_files: int
    log_files: int
    result_files: int
    cache_files: int
    estimated_project_size_kb: int
    health_score: int
    status: str


class PerformanceMonitor:
    def __init__(self, base_dir: str | Path = "."):
        self.base_dir = Path(base_dir)

    def _count_files(self, relative: str) -> int:
        path = self.base_dir / relative
        if not path.exists():
            return 0
        return sum(1 for p in path.rglob("*") if p.is_file())

    def _size_kb(self) -> int:
        total = 0
        skip_names = {".git", "__pycache__"}
        for root, dirs, files in os.walk(self.base_dir):
            dirs[:] = [d for d in dirs if d not in skip_names]
            for name in files:
                try:
                    total += (Path(root) / name).stat().st_size
                except OSError:
                    pass
        return max(1, total // 1024)

    def snapshot(self) -> dict:
        log_files = self._count_files("data/logs")
        result_files = self._count_files("data/results") + self._count_files("data/backtests")
        cache_files = self._count_files("backtest/cache") + self._count_files("data/cache")
        project_files = self._count_files(".")
        size_kb = self._size_kb()

        penalty = min(30, cache_files * 2) + min(20, max(0, log_files - 20)) + min(20, max(0, size_kb // 2048))
        score = max(40, 100 - penalty)
        status = "정상" if score >= 80 else "점검 필요" if score >= 60 else "정리 필요"

        snap = PerformanceSnapshot(
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            python_version=platform.python_version(),
            platform=platform.system(),
            process_id=os.getpid(),
            project_files=project_files,
            log_files=log_files,
            result_files=result_files,
            cache_files=cache_files,
            estimated_project_size_kb=size_kb,
            health_score=score,
            status=status,
        )
        return asdict(snap)
