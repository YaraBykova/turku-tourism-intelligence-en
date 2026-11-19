import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen

try:
    from .statfin_contract import SOURCE_URL, MUNICIPALITIES, METRICS, CSV_COLUMNS, CSV_NAME, parse_response
except ImportError:
    from statfin_contract import SOURCE_URL, MUNICIPALITIES, METRICS, CSV_COLUMNS, CSV_NAME, parse_response


def main():
    with urlopen(SOURCE_URL, timeout=30) as response:
        table = json.load(response)
    variables = {field['code']: field for field in table['variables']}
    municipalities = variables['kunta_86_20190101']
    names = dict(zip(municipalities['values'], municipalities['valueTexts'], strict=True))
    for code, name in MUNICIPALITIES.items():
        if names.get(code) != name:
            raise ValueError(f'Municipality metadata changed: {code}: {names.get(code)}')
    months = variables['timeperiod_m']
    selected = sorted(month for month in months['values'] if month >= '2019M01')
    labels = dict(zip(months['values'], months['valueTexts'], strict=True))
    query = {'query': [
        {'code': 'kunta_86_20190101', 'selection': {'filter': 'item', 'values': list(MUNICIPALITIES)}},
        {'code': 'contentscode', 'selection': {'filter': 'item', 'values': list(METRICS.values())}},
        {'code': 'timeperiod_m', 'selection': {'filter': 'item', 'values': selected}}],
        'response': {'format': 'json-stat2'}}
    request = Request(SOURCE_URL, data=json.dumps(query).encode(),
                      headers={'Content-Type': 'application/json'}, method='POST')
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    received = datetime.now(UTC)
    retrieved_at = received.isoformat(timespec='seconds')
    project = Path(__file__).resolve().parents[1]
    raw = project / 'data/raw/statfin' / f'11lm_{received:%Y%m%dT%H%M%S_%fZ}.json'
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text(json.dumps({'source_url': SOURCE_URL, 'retrieved_at_utc': retrieved_at,
                              'query': query, 'table_metadata': table, 'data_response': result},
                             ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Saved source snapshot: {raw.name}', flush=True)
    rows = parse_response(result, selected, labels, retrieved_at)
    output = project / 'data' / CSV_NAME
    temporary = output.with_suffix('.csv.tmp')
    with temporary.open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(output)
    print(f'Saved {len(rows)} municipality/month rows to {output.name}; {len(selected)} months per city.')


if __name__ == '__main__':
    main()
