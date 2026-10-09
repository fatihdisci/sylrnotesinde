from pathlib import Path
from fontTools.ttLib import TTFont
import json

root = Path(__file__).resolve().parents[1]
reports = []
for path in (root / 'public/fonts').glob('*.woff2'):
    font = TTFont(path)
    cmap = font.getBestCmap()
    required = 'ÖöÜüİıŞşĞğÇç0123456789×→'
    missing = [c for c in required if ord(c) not in cmap]
    reports.append({'file': path.name, 'missing': missing, 'passed': not missing})
assert len(reports) == 5
out = root / 'renders/qa'
out.mkdir(parents=True, exist_ok=True)
(out / 'font-coverage.json').write_text(json.dumps(reports, indent=2, ensure_ascii=False)+'\n')
assert all(r['passed'] for r in reports), reports
print('All 5 local font files contain Turkish, number, multiplication and arrow glyphs.')
