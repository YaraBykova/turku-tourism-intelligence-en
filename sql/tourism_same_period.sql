WITH latest_period AS (
    SELECT
        EXTRACT(YEAR FROM MAX(month))::integer AS latest_year,
        EXTRACT(MONTH FROM MAX(month))::integer AS latest_month
    FROM marts.tourism_seasonality
    WHERE municipality_code = '853'
),

period_totals AS (
    SELECT
        tourism.year,
        COUNT(*) AS months,
        SUM(tourism.hotel_nights) AS hotel_nights
    FROM marts.tourism_seasonality AS tourism
    CROSS JOIN latest_period
    WHERE tourism.municipality_code = '853'
      AND tourism.year IN (
          latest_period.latest_year - 1,
          latest_period.latest_year
      )
      AND tourism.month_number <= latest_period.latest_month
    GROUP BY tourism.year
),

comparison AS (
    SELECT
        year,
        months,
        hotel_nights,
        LAG(hotel_nights) OVER (
            ORDER BY year
        ) AS previous_period_nights
    FROM period_totals
)

SELECT
    year,
    months,
    hotel_nights,
    hotel_nights - previous_period_nights AS change_nights,
    ROUND(
        100.0 * (hotel_nights - previous_period_nights)
        / NULLIF(previous_period_nights, 0),
        2
    ) AS change_pct
FROM comparison
ORDER BY year;
