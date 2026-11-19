import os
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import psycopg
from dotenv import load_dotenv

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

query = """
SELECT month, hotel_nights, is_preliminary
FROM marts.tourism_seasonality
WHERE municipality_code = '853'
ORDER BY month;
"""

by_year = defaultdict(list)
with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=os.getenv("TURKU_POSTGRES_DB", "turku_bi"),
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
) as connection:
    for month, nights, preliminary in connection.execute(query):
        by_year[month.year].append((month.month, nights, preliminary))

if not by_year:
    raise ValueError("No hotel nights found in PostgreSQL for Turku.")

fig, ax = plt.subplots(figsize=(11, 6))

for year, rows in sorted(by_year.items()):
    months, nights, preliminary = zip(*sorted(rows))
    ax.plot(
        months, nights,
        label=f"{year}*" if any(preliminary) else str(year),
        linestyle="--" if any(preliminary) else "-",
    )

ax.set_title("Hotel overnight stays in Turku by month")
ax.set_ylabel("Overnight stays")
ax.set_xticks(range(1, 13), "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())
ax.yaxis.set_major_formatter("{x:,.0f}")
ax.grid(axis="y", alpha=0.25)
ax.legend(ncol=4)

fig.subplots_adjust(bottom=0.19)
fig.text(0.125, 0.09, "Source: Statistics Finland, StatFin 11lm (CC BY 4.0).", fontsize=9)
fig.text(0.125, 0.05, "* Preliminary data. Hotel classification changed in 2025.", fontsize=9)

output = project / "reports" / "turku_hotel_nights_seasonality.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=160)
print(f"Saved {output.name}")
