import json
import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "config" / "version.json"
UPDATES_DIR = ROOT / "updates"
BACKUP_DIR = ROOT / "data" / "backups" / "updates"

DEFAULT_VERSION = {
    "app_name": "DAEJUNGNEXT",
    "version": "v03.3",
    "channel": "beta",
    "safe_update": True,
    "last_checked": "",
}


class UpdateManager:
    def __init__(self):
        self.root = ROOT
        self.version_file = VERSION_FILE
        self.updates_dir = UPDATES_DIR
        self.backup_dir = BACKUP_DIR
        self.updates_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.ensure_version_file()

    def ensure_version_file(self):
        if not self.version_file.exists():
            self.version_file.parent.mkdir(parents=True, exist_ok=True)
            self.save_version(DEFAULT_VERSION)

    def load_version(self):
        self.ensure_version_file()
        with open(self.version_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_version(self, data):
        self.version_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.version_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def check_local_updates(self):
        """updates 폴더에 있는 업데이트 패키지 목록을 확인한다."""
        version = self.load_version()
        version["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_version(version)
        packages = []
        for path in sorted(self.updates_dir.glob("*.zip")):
            packages.append({
                "name": path.name,
                "path": str(path),
                "size": path.stat().st_size,
                "modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
        return packages

    def make_backup(self):
        """업데이트 전 핵심 파일을 백업한다."""
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = self.backup_dir / f"backup_before_update_{stamp}"
        target.mkdir(parents=True, exist_ok=True)
        for name in ["main.py", "core", "services", "ui", "config", "plugins", "docs", "tools"]:
            src = self.root / name
            if not src.exists():
                continue
            dst = target / name
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        return str(target)

    def simulate_update(self):
        """실제 파일 덮어쓰기 없이 업데이트 절차를 테스트한다."""
        backup_path = self.make_backup()
        packages = self.check_local_updates()
        return {
            "success": True,
            "message": "업데이트 시뮬레이션 완료",
            "backup_path": backup_path,
            "packages_found": len(packages),
        }
