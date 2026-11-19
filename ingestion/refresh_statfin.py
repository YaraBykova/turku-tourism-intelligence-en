import subprocess
import sys
from pathlib import Path

project = Path(__file__).resolve().parents[1]

for script in (
    "ingestion/statfin.py",
    "ingestion/check_statfin_quality.py",
    "ingestion/load_statfin_postgres.py",
    "ingestion/build_marts.py",
    "analysis/plot_seasonality.py",
    "analysis/plot_monthly_change.py",
    "analysis/plot_segment_seasonality.py",
):
    subprocess.run([sys.executable, script], cwd=project, check=True)

print("StatFin refresh completed.")
