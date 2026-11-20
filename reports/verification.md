# Verification and scope

The English edition contains the same source data, SQL and numeric calculations as the Russian project. The results below distinguish the original pipeline checks from checks of its English presentation.

## Three-city pipeline

On 19 November 2026 the three-city extension was tested against an isolated empty PostgreSQL database, `turku_bi_cities_20261119_46fbd868`, created from `template0`:

- 279 rows loaded: 93 months for each of three cities, January 2019–September 2026.
- Repeating the CSV changed zero rows; a deliberately older snapshot also changed zero.
- Three dbt view models and three dbt tests passed: **PASS=6 WARN=0 ERROR=0**.
- 21 Python tests passed, covering city/month coverage, counts, segment identities, timestamps and JSON-stat dimension ordering and encodings.
- All 93 previous Turku observations matched, and three plots were generated from the test mart.
- The working database remained unchanged during the isolated check. It was subsequently updated deliberately to 279 rows and reconciled again.

The full manual Airflow run `manual__city_comparison_20261119_verification` completed on 19 November at 02:08:30–02:08:51 Europe/Moscow. All seven tasks succeeded on their first attempt. A fresh API snapshot, dbt results and all three PNGs were produced during the run.

## Scheduled run of the earlier one-city version

The actual scheduled run `scheduled__2026-11-18T22:20:00+00:00` succeeded on 19 November 2026 at 01:20:01–01:21:54 Europe/Moscow. The first extraction attempt timed out during the TLS connection to StatFin; the automatic retry succeeded after one minute. All other tasks succeeded on their first attempt. The API returned fresh data; a saved CSV was not substituted for extraction.

The run produced a 93-month CSV, two successful dbt models and two passing tests, and refreshed all three charts. CSV values were reconciled with PostgreSQL. This was the earlier one-city version; the three-city extension was confirmed by the separate manual run above. The daily schedule remains **01:20 Europe/Moscow**.

The computer, Docker and project containers must be running. This check establishes one observed scheduled execution. Power BI import requires a separate refresh.

## Historical empty-database check: one city

On 19 November 2026, the earlier segment-enabled version was checked in `turku_bi_bootstrap_20261119_acc65934`, created from `template0` with no user objects.

- A saved 93-month CSV passed quality checks; eight Python tests passed.
- The loader created the table and loaded 93 rows; repeating the same file changed zero rows.
- Source, staging and mart contained 93 rows each, matching all seven source fields.
- Two dbt models and two tests passed: **PASS=4 WARN=0 ERROR=0**.
- Segment values were nonnegative, required integers, with zero violations of domestic + international = total.
- Incomplete 2026 had nine months and blank annual totals/shares. Complete-year shares summed to approximately 100%, within 0.06 percentage points.
- All three test PNGs were generated in a separate folder and decoded at 1760 × 960 pixels. This historical check did not include a separate visual review of those PNGs.
- Eight invalid operations were rejected: missing or negative segment values, negative total nights, inconsistent segment totals, a date other than the first of the month and a duplicate municipality/month key. Test transactions were rolled back.
- Working-database row and schema hashes, source code, CSV, existing charts and dbt artefacts remained unchanged. Database selection and output paths applied only to test processes.

The earlier 18 November check, before segment tests were added, finished with PASS=3. The later one-city result above was PASS=4; the three-city result was PASS=6.

## Power BI calculations

All 31 measures of the Russian report were executed through query-scoped DAX definitions on a local Power BI engine. There were 612 successful numerical comparisons: 24 city/year rows, 27 monthly comparisons and 12 monthly points per city for the 2025 profiles under selected 2025 and 2026. Checks included matched prior periods, segment contributions, 100% profile totals and blank comparisons where 2018 baselines are absent.

The corrected Russian layout was confirmed, including seven table columns and three city rows. These checks were completed after correcting the third page to 1600 × 1000 and removing the table's hierarchy flag that hid numeric columns.

## English-edition checks

- 53 report-definition JSON files passed official Microsoft schemas.
- TmdlSerializer parsed the `en-GB` model: 31 measures and 16 Tourism columns; relationships resolved.
- All 25 numeric-measure expressions match the verified Russian edition. Six text measures, month/city labels and culture settings were translated separately.
- Source CSV and JSON snapshots, SQL and numeric pipeline logic were preserved.
- 21 Python tests passed. Local documentation links and visual field references resolved; all three pages remained 1600 × 1000 with no detected overlaps or out-of-page elements.
- The comparison table retains all seven columns and has no hierarchy `active` flag.
- The real `.env`, `.pbi` caches, generated dbt files and old PBIX are omitted. `.env.example`, `.gitignore` and pinned `requirements.txt` are included.

The English report was opened and all three pages were reviewed. Model culture and report locale are `en-GB`; count axes explicitly use full values. The final English and Russian PDFs were checked across all three pages and use aligned years: Overview 2026, Seasonality 2025, and City comparison 2026 with a labelled 2025 profile. English decimal points, thousands separators, full count-axis values, the seven-column table and 12-month profiles were confirmed.

The numerical DAX-engine checks above were performed on the Russian report. English numeric expressions match; a separate execution of all English text measures on the engine is not claimed.

## Boundaries

Existing containers were used for the integration checks. A complete cold installation on another computer has not been verified. A scheduled run of the three-city extension is not established by the earlier one-city scheduled result.

The two repositories and PDFs are public. This does not mean publication to Power BI Service. The English PBIP can use the existing local database; no second running Docker deployment was configured.

Dates and values in analytical Markdown files identify snapshots. Their prose is not updated automatically by the pipeline. Source provenance is preserved in `data/raw/statfin/`; original local audit logs remain in the project's separate notes archive.
