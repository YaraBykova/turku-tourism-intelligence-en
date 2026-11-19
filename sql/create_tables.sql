CREATE TABLE IF NOT EXISTS public.hotel_nights_monthly (
    municipality_code text NOT NULL,
    month date NOT NULL CHECK (EXTRACT(DAY FROM month) = 1),
    hotel_nights integer NOT NULL CHECK (hotel_nights >= 0),
    is_preliminary boolean NOT NULL,
    retrieved_at_utc timestamptz NOT NULL,
    PRIMARY KEY (municipality_code, month)
);

ALTER TABLE public.hotel_nights_monthly
    ADD COLUMN IF NOT EXISTS domestic_nights integer
        CHECK (domestic_nights >= 0),
    ADD COLUMN IF NOT EXISTS foreign_nights integer
        CHECK (foreign_nights >= 0);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'public.hotel_nights_monthly'::regclass
          AND conname = 'hotel_nights_segments_match'
    ) THEN
        ALTER TABLE public.hotel_nights_monthly
            ADD CONSTRAINT hotel_nights_segments_match
            CHECK (domestic_nights + foreign_nights = hotel_nights);
    END IF;
END;
$$;
