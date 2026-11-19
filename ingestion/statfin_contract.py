"""StatFin 11lm contract: municipality × month, three additive counts."""
from datetime import date, datetime
import re

SOURCE_URL = 'https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/matk/11lm.px'
MUNICIPALITIES = {'853': 'Turku', '837': 'Tampere', '564': 'Oulu'}
METRICS = {'hotel_nights': 'yopyneet', 'domestic_nights': 'yopyneet_fi', 'foreign_nights': 'yopyneet_ul'}
CSV_COLUMNS = ['municipality_code', 'month', *METRICS, 'is_preliminary', 'retrieved_at_utc']
CSV_NAME = 'hotel_nights_monthly.csv'


def validate_rows(rows):
    if not rows:
        raise ValueError('CSV is empty.')
    coverage = {code: set() for code in MUNICIPALITIES}
    timestamps = set()
    for line, row in enumerate(rows, start=2):
        code = row.get('municipality_code')
        if code not in coverage:
            raise ValueError(f'Unknown municipality_code in CSV line {line}: {code}')
        month_text = row.get('month', '')
        if not re.fullmatch(r'\d{4}-\d{2}', month_text):
            raise ValueError(f'Invalid month in CSV line {line}')
        month = date.fromisoformat(month_text + '-01')
        ordinal = month.year * 12 + month.month
        if ordinal in coverage[code]:
            raise ValueError(f'Duplicate municipality/month: {code}, {month_text}')
        coverage[code].add(ordinal)
        values = {}
        for column in METRICS:
            value = row.get(column)
            if not isinstance(value, str) or not re.fullmatch(r'-?\d+', value):
                raise ValueError(f'Invalid {column} in CSV line {line}')
            values[column] = int(value)
            if values[column] < 0:
                raise ValueError(f'Negative {column} in CSV line {line}')
        if values['domestic_nights'] + values['foreign_nights'] != values['hotel_nights']:
            raise ValueError(f'Domestic and foreign nights do not add up in CSV line {line}')
        if row.get('is_preliminary') not in {'True', 'False'}:
            raise ValueError(f'Invalid is_preliminary in CSV line {line}')
        try:
            timestamp = datetime.fromisoformat(row['retrieved_at_utc'])
            if timestamp.utcoffset() is None:
                raise ValueError('Timestamp must contain timezone')
        except (KeyError, ValueError, TypeError):
            raise ValueError(f'Invalid retrieved_at_utc in CSV line {line}') from None
        timestamps.add(timestamp)
    if any(not months for months in coverage.values()):
        raise ValueError('Missing expected municipality.')
    latest = max(max(months) for months in coverage.values())
    expected = set(range(2019 * 12 + 1, latest + 1))
    if any(months != expected for months in coverage.values()):
        raise ValueError('Expected consecutive months starting from 2019-01 and identical coverage for every municipality.')
    if len(timestamps) != 1:
        raise ValueError('Expected one retrieval timestamp for the complete snapshot.')


def parse_response(result, selected_months, month_labels, retrieved_at):
    """Resolve JSON-stat coordinates explicitly; missing/suppressed is never zero."""
    expected_categories = {'kunta_86_20190101': set(MUNICIPALITIES),
                           'contentscode': set(METRICS.values()),
                           'timeperiod_m': set(selected_months)}
    if set(result['id']) != set(expected_categories):
        raise ValueError('Unexpected StatFin dimensions.')
    indices = {}
    for code, size in zip(result['id'], result['size'], strict=True):
        index = result['dimension'][code]['category']['index']
        if isinstance(index, list):
            index = {value: i for i, value in enumerate(index)}
        if set(index) != expected_categories[code] or sorted(index.values()) != list(range(size)):
            raise ValueError(f'Unexpected or missing categories: {code}')
        indices[code] = index
    rows = []
    for municipality in MUNICIPALITIES:
        for month in selected_months:
            row = {'municipality_code': municipality, 'month': month.replace('M', '-'),
                   'is_preliminary': str(month_labels[month].endswith('*')),
                   'retrieved_at_utc': retrieved_at}
            for column, metric in METRICS.items():
                coordinates = {'kunta_86_20190101': municipality, 'contentscode': metric, 'timeperiod_m': month}
                position = 0
                for code, size in zip(result['id'], result['size'], strict=True):
                    position = position * size + indices[code][coordinates[code]]
                values = result['value']
                value = values.get(str(position)) if isinstance(values, dict) else values[position]
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    raise ValueError(f'Invalid nights value: {municipality}, {month}, {metric}: {value}')
                row[column] = str(value)
            rows.append(row)
    validate_rows(rows)
    return rows
