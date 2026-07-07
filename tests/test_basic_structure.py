from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_main_exists():
    assert (ROOT / "main.py").exists()

def test_core_exists():
    assert (ROOT / "core" / "state_manager.py").exists()
    assert (ROOT / "core" / "safety_guard.py").exists()

def test_config_exists():
    assert (ROOT / "config" / "config.json").exists()
