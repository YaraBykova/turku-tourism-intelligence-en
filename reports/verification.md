# Verification and scope

The English edition is a separate translation of the three-city project. Source data, SQL and numeric calculations are preserved. The Russian working folder and its database are not modified by the translation.

## Established checks of the original pipeline

On 19 November 2026 the three-city extension was tested against an isolated empty PostgreSQL database created from `template0`:

- 279 rows loaded: 93 months for each of three cities, January 2019–September 2026.
- Repeating the same CSV changed zero rows; a deliberately older snapshot also changed zero.
- Three dbt view models and three dbt tests passed (`PASS=6`).
- 21 Python tests passed, covering city/month coverage, counts, segment identities, timestamps and JSON-stat dimension ordering/encodings.
- All 93 Turku business values matched the previous version, and three plots were generated from the test mart.
- The working database was unchanged during the isolated test. It was subsequently updated deliberately to 279 rows and checked again.

The full manual Airflow run `manual__city_comparison_20261119_verification` completed on 19 November at 02:08:30–02:08:51 Europe/Moscow. All seven tasks succeeded on their first attempt. A fresh API snapshot, dbt results and all three PNGs were produced within the run.

A scheduled run of the earlier one-city version succeeded at 01:20:01–01:21:54 Europe/Moscow, with a retry following a TLS timeout. The three-city extension's seven-task confirmation was manual; a scheduled run of that extension is not claimed here. The schedule remains daily at 01:20 Europe/Moscow.

All 31 measures of the Russian report were executed through query-scoped DAX definitions on a local Power BI engine. There were 612 successful numerical comparisons: 24 city/year rows, 27 monthly comparisons, and 12 monthly points per city for the 2025 profiles under selected 2025 and 2026. The corrected Russian layout was confirmed by user-supplied images, including seven table columns and three city rows.

## English-edition checks

The final validation record for this edition is recorded separately after the translation is built. It checks source/data identity, the 25 unchanged numeric-measure expressions, translated model metadata, official JSON schemas, report geometry, field references, local documentation links, Python tests, and exclusion of known credentials/caches. No screenshots are created for these checks.

## Boundaries

Existing Docker containers were used for the original integration tests. Full cold installation on another computer has not been verified. The English copy does not start another Docker deployment, load another working database, or publish anything.

The translated report contains no imported cache. Its English visual appearance must be checked after opening the English PBIP in Power BI Desktop and selecting Refresh. Verification of the Russian layout does not establish that every longer English label fits.

Dates and values in the analytical Markdown files identify a snapshot, not a live text report. The original local audit logs and backups are retained outside this distributable folder. Data provenance is preserved in `data/raw/statfin/`; raw responses are copied unchanged.

## English edition: completed checks

- 53 report-definition JSON files passed cached official Microsoft schemas.
- TmdlSerializer parsed the English `en-GB` model: 31 measures and 16 Tourism columns; relationships resolved.
- All 25 numeric-measure expressions are byte-identical to the verified Russian edition. Six text measures were translated; month/city labels and model culture were translated separately.
- 41 core code/data files, the SQL models, Compose configuration and dependency/build settings match the source where no translation was required. Source JSON responses and CSV files are byte-identical.
- 21 Python tests passed. Python files parse, local Markdown links resolve, visual field references resolve, all three pages retain 1600 × 1000 dimensions, and no visual overlaps or out-of-page elements were found.
- The seven-column comparison table retains all projections and has no hierarchy `active` flag.
- No remaining Russian text was found in the translated project files (raw API responses are preserved unchanged). Known values from the local credential file were not found in the English text files.
- The real `.env`, all `.pbi` settings/caches, generated dbt files and old PBIX are omitted. A placeholder `.env.example`, `.gitignore` and pinned `requirements.txt` are included.
- Russian source-file hashes were checked before deployment and remained unchanged.

The Power BI engine was closed during the English-edition checks: English DAX captions have not been executed on the engine, and the English visual appearance is pending a Desktop check. This does not replace or repeat the original three-city integration run. No extra containers, database writes, Git repository or publication were created.

## English report locale and user-provided visual confirmation

The user opened the English edition and supplied images of all three pages: English captions and month names are visible, check values match, the comparison table contains all seven columns and three cities, and the 12-month 2025 profiles are displayed under selected 2026. These are user-provided images, not screenshots created by the agent. They also showed Russian auto-unit labels and decimal commas inherited from the viewer environment.

The English model already used en-GB. The report now explicitly sets `settings.locale` to `en-GB` as well, validated against the official report schema. Numeric measures, values, filters and page geometry were not changed. See [Microsoft's report format-string locale documentation](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-default-format-string-locale). Close the old open report without saving over the file correction, reopen the same English PBIP, and check decimal separators and auto-unit labels. This last formatting correction has not yet been confirmed visually.

## Count-axis display units

After the report-locale correction, the user confirmed English number formatting on the seasonality page (822,620 and 35.36% / 38.94%). Automatic chart-unit abbreviations still appeared in Russian. The three count axes on Overview and Seasonality now explicitly use Display units = None and zero decimal places, showing full values such as 50,000 and 100,000. Percentage/profile/contribution axes, query bindings, calculations and visual positions are unchanged. The corrected definitions passed the official visual schema. Reopening the English PBIP is required; the latest axis correction is pending user confirmation.
