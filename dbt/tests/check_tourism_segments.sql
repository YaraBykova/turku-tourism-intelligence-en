SELECT
    municipality_code,
    month
FROM {{ ref('tourism_seasonality') }}
WHERE domestic_nights IS NULL
   OR foreign_nights IS NULL
   OR domestic_nights < 0
   OR foreign_nights < 0
   OR domestic_nights + foreign_nights <> hotel_nights
   OR (
       hotel_nights > 0
       AND (
           foreign_nights_share_pct IS NULL
           OR foreign_nights_share_pct < 0
           OR foreign_nights_share_pct > 100
       )
   )
   OR (
       hotel_nights = 0
       AND foreign_nights_share_pct IS NOT NULL
   )
