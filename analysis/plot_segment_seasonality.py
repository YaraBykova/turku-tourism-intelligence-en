import calendar
import os
from pathlib import Path

import matplotlib.pyplot as plt
import psycopg
from dotenv import load_dotenv


def create_figure(rows):
    if len(rows) != 12:
        raise ValueError("Expected 12 months for the segment comparison.")

    year = rows[0][0].year
    months = [row[0].month for row in rows]
    preliminary = any(row[5] for row in rows)
    domestic_shares = [float(row[3]) for row in rows]
    foreign_shares = [float(row[4]) for row in rows]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(
        months, domestic_shares,
        marker="o", color="#2166AC", label="Domestic nights",
    )
    ax.plot(
        months, foreign_shares,
        marker="o", color="#D97706", label="Foreign nights",
    )
    suffix = "*" if preliminary else ""
    ax.set_title(f"Seasonal profile of hotel nights in Turku, {year}{suffix}")
    ax.set_ylabel("Share of each segment's annual nights (%)")
    ax.set_xticks(months, [calendar.month_abbr[month] for month in months])
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.25)
    ax.legend()

    fig.subplots_adjust(bottom=0.23)
    fig.text(
        0.125, 0.12,
        "Source: Statistics Finland, StatFin 11lm (CC BY 4.0).",
        fontsize=9,
    )
    fig.text(
        0.125, 0.08,
        "Each segment is normalized separately to its annual total.",
        fontsize=9,
    )
    if preliminary:
        fig.text(
            0.125, 0.04,
            "* Comparison includes preliminary data.",
            fontsize=9,
        )
    return fig


def main():
    project = Path(__file__).resolve().parents[1]
    load_dotenv(project / ".env")
    query = (project / "sql" / "tourism_segment_seasonality.sql").read_text(
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

    fig = create_figure(rows)
    output = project / "reports" / "turku_hotel_nights_segment_seasonality.png"
    output.parent.mkdir(exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)
    print(f"Saved {output.name}")


if __name__ == "__main__":
    main()
