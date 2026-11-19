WITH annual_context AS (
    SELECT
        municipality_code,
        month,
        year,
        month_number,
        hotel_nights,
        domestic_nights,
        foreign_nights,
        is_preliminary,
        retrieved_at_utc,
        COUNT(*) OVER year_window AS months_in_year,
        SUM(hotel_nights) OVER year_window AS observed_year_nights
    FROM {{ ref('stg_statfin_hotel_nights') }}
    WINDOW year_window AS (
        PARTITION BY municipality_code, year
    )
)

SELECT
    municipality_code,
    month,
    year,
    month_number,
    hotel_nights,
    is_preliminary,
    retrieved_at_utc,
    months_in_year,
    months_in_year = 12 AS is_complete_year,
    CASE WHEN months_in_year = 12
        THEN observed_year_nights
    END AS year_total_nights,
    CASE WHEN months_in_year = 12
        THEN ROUND(
            100.0 * hotel_nights / NULLIF(observed_year_nights, 0),
            2
        )
    END AS month_share_pct,
    domestic_nights,
    foreign_nights,
    ROUND(
        100.0 * foreign_nights / NULLIF(hotel_nights, 0),
        2
    ) AS foreign_nights_share_pct
FROM annual_context
