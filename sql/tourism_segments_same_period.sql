WITH latest_period AS (
    SELECT
        MAX(year) AS latest_year,
        MAX(month_number) FILTER (
            WHERE year = (
                SELECT MAX(year)
                FROM marts.tourism_seasonality
                WHERE municipality_code = '853'
            )
        ) AS latest_month
    FROM marts.tourism_seasonality
    WHERE municipality_code = '853'
),

period_totals AS (
    SELECT
        tourism.year,
        COUNT(*) AS months,
        SUM(tourism.hotel_nights) AS hotel_nights,
        SUM(tourism.domestic_nights) AS domestic_nights,
        SUM(tourism.foreign_nights) AS foreign_nights
    FROM marts.tourism_seasonality AS tourism
    CROSS JOIN latest_period
    WHERE tourism.municipality_code = '853'
      AND tourism.year IN (
          latest_period.latest_year - 1,
          latest_period.latest_year
      )
      AND tourism.month_number <= latest_period.latest_month
    GROUP BY tourism.year
)

SELECT
    year,
    months,
    hotel_nights,
    domestic_nights,
    foreign_nights,
    ROUND(
        100.0 * foreign_nights / NULLIF(hotel_nights, 0),
        2
    ) AS foreign_share_pct,
    domestic_nights - LAG(domestic_nights) OVER (
        ORDER BY year
    ) AS domestic_change,
    foreign_nights - LAG(foreign_nights) OVER (
        ORDER BY year
    ) AS foreign_change
FROM period_totals
ORDER BY year;
