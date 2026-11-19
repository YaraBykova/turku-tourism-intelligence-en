import os
import csv
import subprocess
from pathlib import Path

import psycopg
from dotenv import load_dotenv

try:
    from .statfin_contract import CSV_NAME, validate_rows
except ImportError:
    from statfin_contract import CSV_NAME, validate_rows

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

database = os.getenv("TURKU_POSTGRES_DB", "turku_bi")
dbt_executable = "/home/airflow/dbt-venv/bin/dbt"

if Path(dbt_executable).is_file():
    dbt_command = [dbt_executable]
    dbt_directory = str(project / "dbt")
else:
    dbt_directory = "/opt/turku/dbt"
    dbt_command = [
        "docker", "compose", "exec", "-T",
        "-e", f"TURKU_POSTGRES_DB={database}",
        "airflow",
        dbt_executable,
    ]

subprocess.run(
    [
        *dbt_command,
        "build",
        "--project-dir", dbt_directory,
        "--profiles-dir", dbt_directory,
    ],
    cwd=project,
    check=True,
)

with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=database,
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
    autocommit=True,
) as connection:
    with connection.cursor() as cursor:
        checks_path = project / "sql" / "check_seasonality.sql"
        cursor.execute(checks_path.read_text(encoding="utf-8-sig"))

        with (project / 'data' / CSV_NAME).open(encoding='utf-8-sig', newline='') as file:
            source_rows = list(csv.DictReader(file))
        validate_rows(source_rows)
        cursor.execute("SELECT municipality_code, to_char(month, 'YYYY-MM'), hotel_nights, domestic_nights, foreign_nights FROM marts.tourism_seasonality")
        actual = set(cursor.fetchall())
        expected = {(r['municipality_code'], r['month'], int(r['hotel_nights']), int(r['domestic_nights']), int(r['foreign_nights'])) for r in source_rows}
        if actual != expected:
            raise ValueError('Mart does not match the complete CSV snapshot (keys and three counts).')

print(f"Marts ready via dbt: {len(actual)} municipality/month rows; source values matched.")
