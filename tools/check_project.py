from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "main.py", "ui/main_window.py", "core/state_manager.py", "core/config_manager.py",
    "core/log_manager.py", "services/validation_service.py", "services/pipeline_service.py",
    "config/config.json", "data/logs", "data/results", "data/runtime"
]

missing = []
for item in REQUIRED:
    if not (ROOT / item).exists():
        missing.append(item)

print("DAEJUNGNEXT v03.0 project check")
print("ROOT:", ROOT)
if missing:
    print("MISSING:")
    for m in missing:
        print("-", m)
    raise SystemExit(1)
print("OK: required files/folders exist")
