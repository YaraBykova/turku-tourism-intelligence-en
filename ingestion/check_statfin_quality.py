import csv
from pathlib import Path

try:
    from .statfin_contract import CSV_NAME, validate_rows
except ImportError:
    from statfin_contract import CSV_NAME, validate_rows


if __name__ == '__main__':
    project = Path(__file__).resolve().parents[1]
    with (project / 'data' / CSV_NAME).open(encoding='utf-8-sig', newline='') as file:
        rows = list(csv.DictReader(file))
    validate_rows(rows)
    print(f'Data quality passed: {len(rows)} municipality/month rows.')
