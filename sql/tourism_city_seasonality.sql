-- Last year with twelve months for every city. Exact (unrounded) segment ratios.
WITH complete_year AS (
    SELECT MAX(year) AS year FROM (
        SELECT year FROM marts.tourism_seasonality GROUP BY year
        HAVING COUNT(DISTINCT municipality_code) = 3 AND BOOL_AND(is_complete_year)
    ) complete
)
SELECT municipality_code, year, SUM(hotel_nights) AS hotel_nights,
    100.0 * SUM(hotel_nights) FILTER (WHERE month_number IN (6,7,8)) / NULLIF(SUM(hotel_nights),0) AS summer_total_pct,
    100.0 * SUM(domestic_nights) FILTER (WHERE month_number IN (6,7,8)) / NULLIF(SUM(domestic_nights),0) AS summer_domestic_pct,
    100.0 * SUM(foreign_nights) FILTER (WHERE month_number IN (6,7,8)) / NULLIF(SUM(foreign_nights),0) AS summer_foreign_pct,
    (array_agg(month_number ORDER BY hotel_nights DESC, month_number))[1] AS peak_month
FROM marts.tourism_seasonality WHERE year = (SELECT year FROM complete_year)
GROUP BY municipality_code, year ORDER BY municipality_code;
