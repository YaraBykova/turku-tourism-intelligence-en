import csv
import os
from datetime import date, datetime
from pathlib import Path

import psycopg
from dotenv import load_dotenv

try:
    from .statfin_contract import CSV_NAME, validate_rows
except ImportError:
    from statfin_contract import CSV_NAME, validate_rows

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

with (project / "data" / CSV_NAME).open(encoding="utf-8-sig", newline="") as file:
    csv_rows = list(csv.DictReader(file))
validate_rows(csv_rows)
rows = [
    (row["municipality_code"], date.fromisoformat(row["month"] + "-01"),
     int(row["hotel_nights"]), int(row["domestic_nights"]), int(row["foreign_nights"]),
     {"True": True, "False": False}[row["is_preliminary"]],
     datetime.fromisoformat(row["retrieved_at_utc"]))
    for row in csv_rows
]

sql = """
INSERT INTO public.hotel_nights_monthly (
    municipality_code,
    month,
    hotel_nights,
    domestic_nights,
    foreign_nights,
    is_preliminary,
    retrieved_at_utc
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (municipality_code, month) DO UPDATE
SET hotel_nights = EXCLUDED.hotel_nights,
    domestic_nights = EXCLUDED.domestic_nights,
    foreign_nights = EXCLUDED.foreign_nights,
    is_preliminary = EXCLUDED.is_preliminary,
    retrieved_at_utc = EXCLUDED.retrieved_at_utc
WHERE EXCLUDED.retrieved_at_utc > hotel_nights_monthly.retrieved_at_utc
   OR (
       EXCLUDED.retrieved_at_utc = hotel_nights_monthly.retrieved_at_utc
       AND (
           hotel_nights_monthly.domestic_nights IS NULL
           OR hotel_nights_monthly.foreign_nights IS NULL
       )
   );
"""

with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=os.getenv("TURKU_POSTGRES_DB", "turku_bi"),
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
) as connection:
    with connection.cursor() as cursor:
        schema_path = project / "sql" / "create_tables.sql"
        cursor.execute(schema_path.read_text(encoding="utf-8-sig"))

        cursor.executemany(sql, rows)
        changed = cursor.rowcount

        cursor.execute("""
            ALTER TABLE public.hotel_nights_monthly
                ALTER COLUMN domestic_nights SET NOT NULL,
                ALTER COLUMN foreign_nights SET NOT NULL;
        """)

print(f"Rows read: {len(rows)}. Rows changed in PostgreSQL: {changed}.")
