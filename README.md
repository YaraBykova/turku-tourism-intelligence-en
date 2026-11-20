# Turku Business Intelligence

[View the dashboard as a 3-page PDF](turku_tourism_dashboard.pdf)

This project demonstrates the complete workflow for open data: API extraction, preservation of raw responses, data-quality checks, loading into PostgreSQL, analytical models in dbt and refresh orchestration with Airflow.

The main analytical question is: **how have hotel nights in Turku changed relative to Tampere and Oulu, and how much have domestic and international nights contributed to that change?**

January–September 2026 versus the same months of 2025: Turku **+6.66%**, Tampere **+0.49%**, Oulu **+13.40%**. Domestic and international nights contributed almost equally to Turku's increase; domestic nights accounted for most of Oulu's increase. The causes of these differences have not been established. [City comparison, methodology and limitations](reports/city_comparison.md).

The project is intended for a DE / DA portfolio: a reproducible pipeline, SQL analysis and Power BI.

## First analytical result

In every complete year from 2019 to 2025, hotel nights in Turku peaked in July. This shows the seasonality of hotel demand, which should be considered when analysing the tourism market.

![Monthly hotel nights in Turku](reports/turku_hotel_nights_seasonality.png)

As of 19 November 2026, the dataset contains 279 rows: 93 months per city (January 2019–September 2026) for Turku, Tampere and Oulu. Subsequent pipeline refreshes request data through the latest published month.

Source: [Statistics Finland, StatFin 11lm](https://pxdata.stat.fi/PXWeb/pxweb/en/StatFin/StatFin__matk/11lm.px), licensed under CC BY 4.0.

Indicator limitations:

- Hotel nights count overnight stays, not unique tourists.
- Data for 2026 are preliminary and may be revised.
- Hotel classification changed in 2025, so comparisons with earlier years require caution.

## Changes in hotel nights

January–September 2026 recorded 689,463 hotel nights, compared with 646,423 in the same months of 2025. The increase was **43,040 nights, or 6.66%**.

Growth occurred in seven of the nine months. January had the largest absolute increase: **+12,121 nights**. April and May declined, with a combined decrease of **6,832 nights**.

![Monthly changes in hotel nights](reports/turku_hotel_nights_monthly_change.png)

The comparison uses the same calendar months. Data for 2026 are preliminary and may be revised. The calculation describes the change in hotel nights over matched periods.

The chart is generated from PostgreSQL and refreshed by the Airflow task `plot_monthly_change`. A successful run of the complete seven-task chain was confirmed on 18 November 2026.

## Domestic and international nights

In January–September 2026, domestic nights increased by **21,354 (+3.96%)** and international nights by **21,686 (+20.28%)** compared with the same months of 2025. The international share rose from **16.54% to 18.65%**.

In 2025, June–August accounted for **35.36%** of annual domestic nights and **38.94%** of annual international nights. Each segment in the chart is normalised to its own annual total.

![Seasonality of domestic and international hotel nights](reports/turku_hotel_nights_segment_seasonality.png)

The chart selects the latest year with 12 months of data. If any values are preliminary, it marks the year with an asterisk and displays a note.

Detailed findings and limitations: [analytical report](reports/tourism_findings.md).

## Pipeline structure

```text
StatFin API
    → raw JSON and CSV
    → data-quality checks
    → PostgreSQL: public.hotel_nights_monthly
    → dbt: marts.stg_statfin_hotel_nights
    → dbt: marts.tourism_seasonality
    → dbt: marts.tourism_city_comparison
    → three dbt tests and SQL reconciliation
    → three charts
```

Raw API responses are saved as separate timestamped JSON files in `data/raw/statfin/`.

The CSV `data/hotel_nights_monthly.csv` contains `municipality_code`, month, three hotel-night counts, a preliminary-data flag and the retrieval time in UTC. Codes: 853 — Turku, 837 — Tampere, 564 — Oulu. Every city must have identical, consecutive monthly coverage from January 2019. This file replaced `turku_hotel_nights.csv`; earlier raw JSON snapshots are preserved.

Each PostgreSQL record represents one municipality and month. Loading the same CSV again creates no duplicates. A newer snapshot can update previously published values.

## dbt models

The dbt source is `public.hotel_nights_monthly`, populated by the Python loader.

Models:

- `marts.stg_statfin_hotel_nights` — source metrics with separate year and month-number fields.
- `marts.tourism_seasonality` — a mart containing the three hotel-night counts, months per year, a complete-year flag, annual totals, monthly shares and the international share.

Annual totals and monthly annual shares are calculated only for years with 12 months of data. These fields remain blank for incomplete years.

- `marts.tourism_city_comparison` — observed-year totals, the same months of the previous year, growth, shares and segment contributions in percentage points.

All three models are PostgreSQL views.

## Reproducing the results

Python 3.14 and a running Docker Desktop are required.

Create a `.env` file in the project root and set the PostgreSQL password:

```dotenv
TURKU_POSTGRES_PASSWORD=your_local_password
```

Replace `your_local_password` with your own password. `.env` is excluded from Git by `.gitignore`.

Run these commands from the project root on Windows:

```powershell
py -3.14 -m pip install matplotlib==3.11.2 "psycopg[binary]==3.3.9" python-dotenv==1.2.4
docker compose up -d --build
py -3.14 ingestion/refresh_statfin.py
```

The pipeline runs these steps in order:

1. Retrieves StatFin data from January 2019 through the latest published month.
2. Saves the raw response and CSV.
3. Checks CSV quality.
4. Loads the data into PostgreSQL.
5. Builds three dbt models, runs three dbt tests and performs SQL reconciliation.
6. Generates three charts from the PostgreSQL mart.

Charts are saved to:

```text
reports/turku_hotel_nights_seasonality.png
reports/turku_hotel_nights_monthly_change.png
reports/turku_hotel_nights_segment_seasonality.png
```

Compose includes a PostgreSQL health check; Airflow starts after that check succeeds.

dbt is installed inside the Airflow container. `build_marts.py` supports execution from Windows and inside the container.

To build the models and run their checks separately:

```powershell
py -3.14 ingestion/build_marts.py
```

## Refreshing with Airflow

DAG `turku_tourism` executes seven sequential tasks:

1. `extract_statfin` — retrieves total, domestic and international nights; saves the raw response and CSV.
2. `check_data_quality` — checks the CSV before loading.
3. `load_postgres` — loads the data into PostgreSQL.
4. `build_marts` — builds three dbt models and runs three tests.
5. `plot_seasonality` — charts overall monthly seasonality by year.
6. `plot_monthly_change` — charts changes against the same months of the previous year.
7. `plot_segment_seasonality` — compares domestic and international seasonality.

After starting the project containers, Airflow is available locally at `http://localhost:8080`.

On 18 November 2026, a successful manual run of all seven tasks was confirmed for the earlier one-city version, with 93 months in the mart.

The daily schedule is **01:20 Europe/Moscow** (`20 1 * * *`).
On 19 November 2026, an actual scheduled run of that one-city version succeeded: all seven tasks completed at 01:20:01–01:21:54 Europe/Moscow, two dbt models and two tests passed, and the CSV and three charts were refreshed.
The first StatFin connection attempt timed out; the automatic retry succeeded.
Details: [verification](reports/verification.md#scheduled-run-of-the-earlier-one-city-version).

The computer, Docker Desktop and project containers must be running for the schedule to execute.

## Data-quality checks

Before loading into PostgreSQL, `check_data_quality` checks:

- Nonempty data and consecutive monthly coverage from January 2019 for each city.
- No duplicate municipality/month records.
- Nonnegative integer counts for total, domestic and international nights.
- Domestic plus international nights equal total nights.
- Valid preliminary-data flags.

The current suite contains 21 Python tests, covering the data contract and JSON-stat parsing, including empty input, negative values, duplicates, missing months or cities, missing metrics, inconsistent segment totals and dimension ordering.

Run:

```powershell
py -3.14 -m unittest discover -s tests -v
```

`dbt build` runs three tests:

- `check_tourism_seasonality` — checks months and annual shares. Complete-year shares must sum to approximately 100%, within 0.06 percentage points; incomplete-year shares remain blank.
- `check_tourism_segments` — checks required, nonnegative segment values, their sum against the total and valid international-share bounds.
- `check_city_comparison` — checks identical city coverage, prior-period baselines, segment sums and contributions to total growth.

PostgreSQL also enforces required values, nonnegative counts and segment totals.

A build or test failure fails `build_marts` and prevents subsequent chart generation.

## Failure-handling check

A simulated extraction failure was tested using this DAG parameter:

```json
{"simulate_source_failure": true}
```

Airflow made three unsuccessful attempts at the first task. Downstream tasks did not run. The previously loaded 93 PostgreSQL records, CSV and chart from that one-city check were preserved.

After disabling the simulation, a new run succeeded.

## Verification of the three-city extension

On 19 November 2026, a fresh API response provided 279 rows. In an isolated empty database, the first load changed 279 rows; repeating it and attempting to load an older snapshot each changed zero. Three dbt models and three tests passed (**PASS=6**); 21 Python tests checked the contract and JSON-stat parsing. All 93 previous Turku observations were preserved, and three charts were rebuilt from the extended mart. A full manual Airflow run on 19 November at 02:08:30–02:08:51 Europe/Moscow succeeded on the first attempt for all seven tasks. Details of the working-database update and verification scope: [verification](reports/verification.md#three-city-pipeline).

## Historical empty-database check: one city

On 19 November 2026, the earlier version with domestic and international nights was checked in a new database, `turku_bi_bootstrap_20261119_acc65934`, created from `template0`.
It contained no user objects before loading.

- The Python loader created the table and loaded 93 months; repeating the same CSV changed zero rows.
- dbt created two models and ran two tests: **PASS=4 WARN=0 ERROR=0**.
- Eight Python tests passed; PostgreSQL constraints rejected eight invalid operations.
- All three charts were generated from the new mart in a separate folder.
- The working database, source files, code, existing charts and dbt artefacts remained unchanged during this check.

This checked the path from a saved CSV to marts and charts in existing containers. It did not verify a full installation on another computer or a scheduled Airflow run.
The historical 18 November run, before segment checks were added, finished with PASS=3; the subsequent two-model, two-test check finished with PASS=4.

Details and scope: [verification](reports/verification.md#historical-empty-database-check-one-city).
`TURKU_POSTGRES_DB` selects the database; its default is `turku_bi`. During the check it was set only for test processes.

## Power BI dashboard

The project root contains `turku_tourism_dashboard.pbip` and its neighbouring `.Report` and `.SemanticModel` folders.

- **01 · Overview:** year selection, segment volumes, international share, changes against the same months of the previous year and two monthly charts.
- **02 · Seasonality:** complete years only, summer shares and monthly segment profiles for Turku.
- **03 · City comparison:** volumes, growth and segment mix for three cities, segment contributions and normalised full-year profiles.

The first two pages use Turku page filters; there is no report-wide Turku filter.

Open the `.pbip` in Power BI Desktop. After Airflow refreshes the database, select **Refresh** in Power BI: its imported model does not refresh automatically with PostgreSQL.
The connection uses the local database `turku_bi` at `127.0.0.1:5433`. PostgreSQL and Docker must be running to refresh it.

On 19 November, report definitions passed Microsoft's schemas, the model was parsed with Analysis Services, and the original report's measures were executed through read-only queries on the local Power BI engine and reconciled with PostgreSQL.
The dashboard contains three pages. All 31 measures passed 612 numerical DAX comparisons. The final English PDF was checked on all three pages and its values match the validated results. View the PDF linked at the top of this README or open the PBIP project in Power BI Desktop.

Calculations and check values: [Power BI](reports/powerbi_dashboard.md).
The earlier PBIX is not included in this English edition; use the PBIP project.

## Language editions

Russian version: [Turku Tourism Intelligence — Russian repository](https://github.com/YaraBykova/turku-tourism-intelligence).

Both editions contain the same data and calculations.
