import calendar
import os
from pathlib import Path

import matplotlib.pyplot as plt
import psycopg
from dotenv import load_dotenv

project = Path(__file__).resolve().parents[1]
load_dotenv(project / ".env")

query = (project / "sql" / "tourism_monthly_change.sql").read_text(
    encoding="utf-8-sig"
)

with psycopg.connect(
    host=os.getenv("TURKU_POSTGRES_HOST", "127.0.0.1"),
    port=os.getenv("TURKU_POSTGRES_PORT", "5433"),
    dbname=os.getenv("TURKU_POSTGRES_DB", "turku_bi"),
    user="turku",
    password=os.environ["TURKU_POSTGRES_PASSWORD"],
    connect_timeout=10,
) as connection:
    rows = connection.execute(query).fetchall()

if not rows:
    raise ValueError("No data found for the monthly comparison.")

if any(row[1] is None for row in rows):
    raise ValueError("Previous-year data is missing for some months.")

year = rows[0][0].year
months = [row[0].month for row in rows]
changes = [row[3] for row in rows]

previous_total = sum(row[1] for row in rows)
total_change = sum(changes)
change_pct = 100.0 * total_change / previous_total

period = (
    f"{calendar.month_abbr[months[0]]}"
    f"–{calendar.month_abbr[months[-1]]}"
)

fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.bar(
    months,
    changes,
    color=["#2166AC" if value >= 0 else "#B2182B" for value in changes],
)

ax.bar_label(
    bars,
    labels=[f"{value:+,}" for value in changes],
    padding=4,
    fontsize=9,
)

ax.set_title(
    f"Turku hotel nights: monthly change, {year} vs {year - 1}\n"
    f"{period}: {total_change:+,} nights ({change_pct:+.2f}%)"
)
ax.set_ylabel("Change in overnight stays")
ax.set_xticks(months, [calendar.month_abbr[month] for month in months])
ax.yaxis.set_major_formatter("{x:,.0f}")
ax.axhline(0, color="#333333", linewidth=0.8)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.2)
ax.margins(y=0.18)

fig.subplots_adjust(bottom=0.19)
fig.text(
    0.125, 0.09,
    "Source: Statistics Finland, StatFin 11lm (CC BY 4.0).",
    fontsize=9,
)

if any(row[5] for row in rows):
    fig.text(
        0.125, 0.05,
        "* Comparison includes preliminary data.",
        fontsize=9,
    )

output = project / "reports" / "turku_hotel_nights_monthly_change.png"
output.parent.mkdir(exist_ok=True)
fig.savefig(output, dpi=160)
plt.close(fig)

print(f"Saved {output.name}")
