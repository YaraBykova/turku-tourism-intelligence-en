SELECT
    municipality_code,
    month,
    EXTRACT(YEAR FROM month)::integer AS year,
    EXTRACT(MONTH FROM month)::integer AS month_number,
    hotel_nights,
    is_preliminary,
    retrieved_at_utc,
    domestic_nights,
    foreign_nights
FROM {{ source('statfin', 'hotel_nights_monthly') }}
