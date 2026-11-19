WITH failures AS (
    SELECT municipality_code, year FROM {{ ref('tourism_city_comparison') }}
    WHERE hotel_nights <> domestic_nights + foreign_nights
        OR nights_change <> domestic_change + foreign_change
        OR ABS(nights_growth_pct - domestic_contribution_pp - foreign_contribution_pp) > 0.00000001
        OR (year = 2019 AND previous_nights IS NOT NULL)
        OR (year > 2019 AND previous_nights IS NULL)
    UNION ALL
    SELECT MIN(municipality_code), year FROM {{ ref('tourism_city_comparison') }}
    GROUP BY year
    HAVING COUNT(*) <> 3 OR COUNT(DISTINCT municipality_code) <> 3
        OR COUNT(DISTINCT period_start) <> 1 OR COUNT(DISTINCT period_last_month) <> 1
        OR COUNT(DISTINCT observed_months) <> 1
)
SELECT * FROM failures
