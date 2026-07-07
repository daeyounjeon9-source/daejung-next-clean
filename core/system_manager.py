from __future__ import annotations

import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / 'config'
DATA_DIR = BASE_DIR / 'data'
BACKUP_DIR = DATA_DIR / 'backups'
EXPORT_DIR = DATA_DIR / 'exports'
LOG_DIR = DATA_DIR / 'logs'
CACHE_DIR = DATA_DIR / 'cache'
RESULT_DIR = DATA_DIR / 'results'
SYSTEM_SETTINGS_FILE = CONFIG_DIR / 'system_settings.json'

for path in [CONFIG_DIR, DATA_DIR, BACKUP_DIR, EXPORT_DIR, LOG_DIR, CACHE_DIR, RESULT_DIR]:
    path.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def get_system_status() -> Dict[str, Any]:
    required = ['main.py', 'ui', 'core', 'services', 'config', 'data']
    checks = {name: (BASE_DIR / name).exists() for name in required}
    return {
        'program': '대정NEXT',
        'version': 'Sprint 5',
        'base_dir': str(BASE_DIR),
        'config_exists': CONFIG_DIR.exists(),
        'project_config_exists': (CONFIG_DIR / 'project.json').exists(),
        'result_count': len(list(RESULT_DIR.glob('**/*.json'))),
        'log_count': len(list(LOG_DIR.glob('*.log'))),
        'backup_count': len(list(BACKUP_DIR.glob('*.zip'))),
        'checks': checks,
        'ok': all(checks.values()),
        'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


def backup_project() -> Path:
    out = BACKUP_DIR / f'daejungnext_backup_{_timestamp()}.zip'
    exclude_dirs = {'__pycache__', '.git', '.venv', 'venv'}
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in BASE_DIR.rglob('*'):
            if not file_path.is_file():
                continue
            if any(part in exclude_dirs for part in file_path.parts):
                continue
            if file_path == out:
                continue
            zf.write(file_path, file_path.relative_to(BASE_DIR))
    return out


def backup_config() -> Path:
    out = BACKUP_DIR / f'config_backup_{_timestamp()}.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in CONFIG_DIR.glob('*.json'):
            zf.write(file_path, file_path.relative_to(BASE_DIR))
    return out


def list_backups() -> List[Path]:
    return sorted(BACKUP_DIR.glob('*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)


def restore_config_from_backup(backup_path: str | Path) -> None:
    backup = Path(backup_path)
    if not backup.exists():
        raise FileNotFoundError(str(backup))
    with zipfile.ZipFile(backup, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('config/') and name.endswith('.json'):
                zf.extract(name, BASE_DIR)


def export_logs() -> Path:
    out = EXPORT_DIR / f'logs_export_{_timestamp()}.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in LOG_DIR.glob('*'):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(BASE_DIR))
    return out


def clear_logs() -> int:
    count = 0
    for file_path in LOG_DIR.glob('*'):
        if file_path.is_file():
            file_path.unlink(missing_ok=True)
            count += 1
    return count


def clear_cache() -> int:
    count = 0
    for file_path in CACHE_DIR.glob('**/*'):
        if file_path.is_file():
            file_path.unlink(missing_ok=True)
            count += 1
    return count


def save_system_settings(settings: Dict[str, Any]) -> Path:
    SYSTEM_SETTINGS_FILE.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')
    return SYSTEM_SETTINGS_FILE


def load_system_settings() -> Dict[str, Any]:
    default = {
        'auto_load_last_project': True,
        'auto_backup_on_exit': False,
        'save_error_log': True,
        'safe_mode': True,
    }
    if SYSTEM_SETTINGS_FILE.exists():
        try:
            data = json.loads(SYSTEM_SETTINGS_FILE.read_text(encoding='utf-8'))
            default.update(data)
        except Exception:
            pass
    return default
