DO $$
BEGIN
    IF EXISTS (
        SELECT municipality_code, year
        FROM marts.tourism_seasonality
        GROUP BY municipality_code, year
        HAVING
            (
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
    ) THEN
        RAISE EXCEPTION 'Seasonality checks failed.';
    END IF;
END;
$$;


SELECT
    year,
    COUNT(*) AS months,
    COUNT(month_share_pct) AS months_with_share,
    SUM(month_share_pct) AS total_share_pct
FROM marts.tourism_seasonality
WHERE municipality_code = '853'
GROUP BY year
ORDER BY year;
