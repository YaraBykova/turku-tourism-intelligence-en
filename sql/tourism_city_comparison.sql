-- Latest available year; same observed months in current and prior year.
SELECT * FROM marts.tourism_city_comparison
WHERE year = (SELECT MAX(year) FROM marts.tourism_city_comparison)
ORDER BY nights_growth_pct DESC NULLS LAST, municipality_code;
