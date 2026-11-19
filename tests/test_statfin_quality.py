import copy
import itertools
import unittest

from ingestion.statfin_contract import MUNICIPALITIES, METRICS, parse_response, validate_rows


class TestStatfinQuality(unittest.TestCase):
    def setUp(self):
        self.rows = [dict(municipality_code=city, month=month, hotel_nights='100',
                          domestic_nights='70', foreign_nights='30', is_preliminary='False',
                          retrieved_at_utc='2026-11-19T00:00:00+00:00')
                     for city in MUNICIPALITIES for month in ['2019-01', '2019-02', '2019-03']]

    def test_valid_three_cities(self):
        validate_rows(self.rows)

    def test_same_month_in_different_cities_is_valid(self):
        validate_rows([r for r in self.rows if r['month'] == '2019-01'])

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, 'CSV is empty'):
            validate_rows([])

    def test_duplicate_city_month(self):
        self.rows.append(self.rows[0].copy())
        with self.assertRaisesRegex(ValueError, 'Duplicate municipality/month'):
            validate_rows(self.rows)

    def test_unknown_city(self):
        self.rows[0]['municipality_code'] = '000'
        with self.assertRaisesRegex(ValueError, 'Unknown municipality'):
            validate_rows(self.rows)

    def test_missing_city(self):
        with self.assertRaisesRegex(ValueError, 'Missing expected municipality'):
            validate_rows(self.rows[:6])

    def test_internal_gap(self):
        self.rows.pop(1)
        with self.assertRaisesRegex(ValueError, 'Expected consecutive months'):
            validate_rows(self.rows)

    def test_missing_last_month_in_one_city(self):
        self.rows.pop()
        with self.assertRaisesRegex(ValueError, 'identical coverage'):
            validate_rows(self.rows)

    def test_missing_first_month(self):
        with self.assertRaisesRegex(ValueError, 'Expected consecutive months'):
            validate_rows([r for r in self.rows if r['month'] != '2019-01'])

    def test_negative_count(self):
        for column in METRICS:
            rows = copy.deepcopy(self.rows)
            rows[0][column] = '-1'
            with self.subTest(column=column), self.assertRaisesRegex(ValueError, 'Negative'):
                validate_rows(rows)

    def test_missing_segment(self):
        del self.rows[0]['foreign_nights']
        with self.assertRaisesRegex(ValueError, 'Invalid foreign_nights'):
            validate_rows(self.rows)

    def test_fractional_count(self):
        self.rows[0]['hotel_nights'] = '100.5'
        with self.assertRaisesRegex(ValueError, 'Invalid hotel_nights'):
            validate_rows(self.rows)

    def test_segment_identity(self):
        self.rows[0]['foreign_nights'] = '31'
        with self.assertRaisesRegex(ValueError, 'do not add up'):
            validate_rows(self.rows)

    def test_invalid_flag(self):
        self.rows[0]['is_preliminary'] = 'maybe'
        with self.assertRaisesRegex(ValueError, 'Invalid is_preliminary'):
            validate_rows(self.rows)

    def test_timestamp_requires_timezone(self):
        self.rows[0]['retrieved_at_utc'] = '2026-11-19T00:00:00'
        with self.assertRaisesRegex(ValueError, 'Invalid retrieved_at_utc'):
            validate_rows(self.rows)

    def test_mixed_snapshots_rejected(self):
        self.rows[0]['retrieved_at_utc'] = '2026-11-18T00:00:00+00:00'
        with self.assertRaisesRegex(ValueError, 'one retrieval timestamp'):
            validate_rows(self.rows)


class TestJsonStat(unittest.TestCase):
    def response(self, dimensions, sparse=False):
        categories = {'kunta_86_20190101': list(MUNICIPALITIES),
                      'contentscode': list(METRICS.values()), 'timeperiod_m': ['2019M01']}
        dimensions = list(dimensions)
        result = {'id': dimensions, 'size': [len(categories[d]) for d in dimensions],
                  'dimension': {d: {'category': {'index': {v: i for i, v in enumerate(categories[d])}}} for d in dimensions}}
        numbers = {'yopyneet': 100, 'yopyneet_fi': 70, 'yopyneet_ul': 30}
        # Distinct city values detect accidentally reading Turku for every coordinate.
        values = [numbers[dict(zip(dimensions, coordinates))['contentscode']] *
                  (list(MUNICIPALITIES).index(dict(zip(dimensions, coordinates))['kunta_86_20190101']) + 1)
                  for coordinates in itertools.product(*(categories[d] for d in dimensions))]
        result['value'] = {str(i): v for i, v in enumerate(values)} if sparse else values
        return result

    def parse(self, result):
        return parse_response(result, ['2019M01'], {'2019M01': '2019M01*'}, '2026-11-19T00:00:00+00:00')

    def test_all_dimension_orders_and_value_encodings(self):
        for order in itertools.permutations(['kunta_86_20190101', 'contentscode', 'timeperiod_m']):
            for sparse in [True, False]:
                with self.subTest(order=order, sparse=sparse):
                    rows = self.parse(self.response(order, sparse))
                    self.assertEqual([r['hotel_nights'] for r in rows], ['100', '200', '300'])
                    self.assertTrue(all(r['is_preliminary'] == 'True' for r in rows))

    def test_category_list_encoding(self):
        result = self.response(['contentscode', 'timeperiod_m', 'kunta_86_20190101'])
        for dimension in result['dimension'].values():
            dimension['category']['index'] = list(dimension['category']['index'])
        self.assertEqual(len(self.parse(result)), 3)

    def test_missing_or_suppressed_value_is_not_zero(self):
        for value in [None, '..', True, 1.5, -1]:
            result = self.response(['kunta_86_20190101', 'contentscode', 'timeperiod_m'])
            result['value'][0] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Invalid nights value'):
                self.parse(result)

    def test_missing_sparse_value_is_not_zero(self):
        result = self.response(['kunta_86_20190101', 'contentscode', 'timeperiod_m'], True)
        del result['value']['0']
        with self.assertRaisesRegex(ValueError, 'Invalid nights value'):
            self.parse(result)

    def test_missing_city_in_api_response(self):
        result = self.response(['kunta_86_20190101', 'contentscode', 'timeperiod_m'])
        del result['dimension']['kunta_86_20190101']['category']['index']['837']
        with self.assertRaisesRegex(ValueError, 'missing categories'):
            self.parse(result)


if __name__ == '__main__':
    unittest.main()
