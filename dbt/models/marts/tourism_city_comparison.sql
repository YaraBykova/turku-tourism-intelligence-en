-- One municipality/year; prior year is restricted to the same observed months.
WITH paired AS (
    SELECT c.*, p.month AS prior_month,
        p.hotel_nights AS prior_nights,
        p.domestic_nights AS prior_domestic,
        p.foreign_nights AS prior_foreign
    FROM {{ ref('tourism_seasonality') }} c
    LEFT JOIN {{ ref('tourism_seasonality') }} p
        ON p.municipality_code = c.municipality_code
        AND p.year = c.year - 1 AND p.month_number = c.month_number
), totals AS (
    SELECT municipality_code, year, MIN(month) AS period_start,
        MAX(month) AS period_last_month, COUNT(*) AS observed_months,
        BOOL_OR(is_preliminary) AS is_preliminary,
        SUM(hotel_nights) AS hotel_nights,
        SUM(domestic_nights) AS domestic_nights,
        SUM(foreign_nights) AS foreign_nights,
        CASE WHEN COUNT(prior_month) = COUNT(*) THEN SUM(prior_nights) END AS previous_nights,
        CASE WHEN COUNT(prior_month) = COUNT(*) THEN SUM(prior_domestic) END AS previous_domestic,
        CASE WHEN COUNT(prior_month) = COUNT(*) THEN SUM(prior_foreign) END AS previous_foreign
    FROM paired
    GROUP BY municipality_code, year
)
SELECT *,
    hotel_nights - previous_nights AS nights_change,
    domestic_nights - previous_domestic AS domestic_change,
    foreign_nights - previous_foreign AS foreign_change,
    100.0 * (hotel_nights - previous_nights) / NULLIF(previous_nights, 0) AS nights_growth_pct,
    100.0 * (domestic_nights - previous_domestic) / NULLIF(previous_domestic, 0) AS domestic_growth_pct,
    100.0 * (foreign_nights - previous_foreign) / NULLIF(previous_foreign, 0) AS foreign_growth_pct,
    100.0 * foreign_nights / NULLIF(hotel_nights, 0) AS foreign_share_pct,
    100.0 * foreign_nights / NULLIF(hotel_nights, 0)
        - 100.0 * previous_foreign / NULLIF(previous_nights, 0) AS foreign_share_change_pp,
    100.0 * (domestic_nights - previous_domestic) / NULLIF(previous_nights, 0) AS domestic_contribution_pp,
    100.0 * (foreign_nights - previous_foreign) / NULLIF(previous_nights, 0) AS foreign_contribution_pp
FROM totals
