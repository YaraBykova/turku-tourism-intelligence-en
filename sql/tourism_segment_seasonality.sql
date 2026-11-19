WITH latest_complete_year AS (
    SELECT MAX(year) AS year
    FROM marts.tourism_seasonality
    WHERE municipality_code = '853'
      AND is_complete_year
)

SELECT
    month,
    domestic_nights,
    foreign_nights,
    ROUND(
        100.0 * domestic_nights
        / NULLIF(SUM(domestic_nights) OVER (), 0),
        2
    ) AS domestic_year_share_pct,
    ROUND(
        100.0 * foreign_nights
        / NULLIF(SUM(foreign_nights) OVER (), 0),
        2
    ) AS foreign_year_share_pct,
    is_preliminary
FROM marts.tourism_seasonality
WHERE municipality_code = '853'
  AND year = (SELECT year FROM latest_complete_year)
ORDER BY month;
