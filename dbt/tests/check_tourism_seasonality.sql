SELECT
    municipality_code,
    year
FROM {{ ref('tourism_seasonality') }}
GROUP BY municipality_code, year
HAVING
    COUNT(*) <> COUNT(DISTINCT month)
    OR COUNT(*) > 12
    OR (
        COUNT(*) = 12
        AND (
            COUNT(month_share_pct) <> 12
            OR ABS(SUM(month_share_pct) - 100) > 0.06
        )
    )
    OR (
        COUNT(*) < 12
        AND COUNT(month_share_pct) > 0
    )
