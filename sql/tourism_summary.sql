SELECT
    year,
    SUM(hotel_nights) AS annual_nights,
    SUM(hotel_nights) FILTER (
        WHERE month_number BETWEEN 6 AND 8
    ) AS summer_nights,
    ROUND(
        100.0 * SUM(hotel_nights) FILTER (
            WHERE month_number BETWEEN 6 AND 8
        ) / NULLIF(SUM(hotel_nights), 0),
        2
    ) AS summer_share_pct,
    ROUND(
        100.0 * SUM(hotel_nights) FILTER (
            WHERE month_number = 7
        ) / NULLIF(SUM(hotel_nights), 0),
        2
    ) AS july_share_pct
FROM marts.tourism_seasonality
WHERE municipality_code = '853'
  AND is_complete_year
GROUP BY year
ORDER BY year;
