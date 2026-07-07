import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / 'data' / 'results'

def save_result(result):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = RESULT_DIR / f'result_{stamp}.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(path)

def load_results(limit=100):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(RESULT_DIR.glob('result_*.json'), reverse=True)[:limit]:
        try:
            rows.append(json.loads(path.read_text(encoding='utf-8')))
        except Exception:
            pass
    return rows
