WITH latest_year AS (
    SELECT MAX(year) AS year
    FROM marts.tourism_seasonality
    WHERE municipality_code = '853'
)

SELECT
    current_period.month,
    previous_period.hotel_nights AS previous_year_nights,
    current_period.hotel_nights AS current_year_nights,
    current_period.hotel_nights
        - previous_period.hotel_nights AS change_nights,
    ROUND(
        100.0 * (
            current_period.hotel_nights
            - previous_period.hotel_nights
        ) / NULLIF(previous_period.hotel_nights, 0),
        2
    ) AS change_pct,
    current_period.is_preliminary
FROM marts.tourism_seasonality AS current_period
LEFT JOIN marts.tourism_seasonality AS previous_period
    ON previous_period.municipality_code
        = current_period.municipality_code
    AND previous_period.year = current_period.year - 1
    AND previous_period.month_number = current_period.month_number
WHERE current_period.municipality_code = '853'
  AND current_period.year = (SELECT year FROM latest_year)
ORDER BY current_period.month;
