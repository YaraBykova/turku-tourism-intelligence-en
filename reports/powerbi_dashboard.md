# Power BI: hotel nights and city comparison

Open `turku_tourism_dashboard.pbip` in the project root. Keep the neighbouring `.Report` and `.SemanticModel` folders alongside it.

## Source and refresh

The report imports `marts.tourism_seasonality` from PostgreSQL: `127.0.0.1:5433`, database `turku_bi`, user `turku`.
Enter the password in Power BI if prompted; credentials are not included in the report definitions. Docker and PostgreSQL must be running to refresh the data.

Airflow refreshes the database and PNG charts. Refresh the Power BI import separately using **Refresh**. Markdown reports record dated analysis and are not rewritten automatically.

## Pages

1. **01 · Overview:** Turku hotel-night volumes, segment mix, international share, changes against the same months of the previous year and monthly charts. Default: 2026.
2. **02 · Seasonality:** complete years only, summer shares and monthly shares of each segment's own annual total. Default: 2025.
3. **03 · City comparison:** three growth cards, a seven-column table, domestic and international contributions to growth and normalised annual city profiles. Default: 2026; while 2026 is incomplete, the profile shows complete 2025.

All pages are 1600 × 1000. The first two use Turku page filters; the third uses all three cities. There is no report-wide Turku filter. Year slicers control the year; selecting chart points does not change the other visuals' comparison periods.

## Calculation rules

- International share is summed international nights divided by summed total nights over the selected period.
- Year-on-year comparisons use only the months observed in the selected year. January–September 2026 is compared with January–September 2025, preserving the selected cities.
- If any required prior-year month is missing, the comparison is blank. There is no 2018 baseline for 2019.
- On the seasonality page, each segment is divided by its own annual total; incomplete years are excluded.
- Segment contribution, pp = (current-period segment nights − prior-period segment nights) / prior-period total nights × 100. Contributions sum to total growth before rounding. A segment's own growth rate uses a different denominator: that segment's prior-period nights.
- In the city profile, each month is divided by that city's annual total. If the selected year is incomplete, the preceding complete year is used and explicitly labelled. A separate `Profile Months` calendar preserves all 12 months on the axis.

The model contains 31 measures and calculated city and month labels. Numeric calculations match in RU and EN; captions and number formatting follow the report's language edition.

## Check values

| Context | Expected |
|---|---:|
| Overview 2026, January–September: total | 689,463 |
| Domestic / international | 560,859 / 128,604 |
| International share | 18.65% |
| Total / domestic / international growth | +6.66% / +3.96% / +20.28% |
| International share change | +2.11 pp |
| Overview 2025, full-year total | 822,620 |
| Seasonality 2025: peak | July |
| Domestic / international summer shares | 35.36% / 38.94% |
| Growth 2026: Turku / Tampere / Oulu | +6.66% / +0.49% / +13.40% |
| Nights 2026: Turku / Tampere / Oulu | 689,463 / 1,023,197 / 449,842 |
| Growth 2025: Turku / Tampere / Oulu | +0.26% / +1.55% / −0.34% |

Under selected 2025 or incomplete 2026, the city profile uses complete 2025. Each city's 12 monthly shares sum to 100% before rounding.

## Completed verification

On 19 November 2026, 53 JSON files passed Microsoft's official schemas and the model was parsed with Analysis Services. All 31 measures of the Russian report were executed through temporary DAX queries on the local Power BI engine and reconciled with PostgreSQL: 612 numerical comparisons passed. Checks covered 24 city/year rows, 27 monthly comparisons and 2025 profiles under selected 2025 and 2026.

In the English edition, 25 numeric-measure expressions match the Russian originals; six text measures and captions were translated. Model culture and report locale are set to `en-GB`, and count axes use full values without automatic unit abbreviations.

Both final PDFs were checked on all three pages: Overview 2026, Seasonality 2025, and City comparison 2026 with a labelled 2025 profile. Values, all seven table columns and three cities, the 12-month profile and English number formatting were confirmed. Earlier page-size and hidden-column corrections have been applied and verified.

## Limitations

Source: Statistics Finland, StatFin 11lm, CC BY 4.0. Data for 2026 are preliminary and may be revised. The 2025 hotel-classification change limits comparability with earlier years.

Hotel nights are not unique tourists, pedestrian footfall or sales. The report is descriptive, without forecasts or causal conclusions. Oulu's European Capital of Culture 2026 status provides context; its effect has not been estimated.

The PDF is available for viewing in the repository. The PBIP is intended for Power BI Desktop; the report has not been published to Power BI Service. The earlier PBIX does not update automatically when PBIP definitions change and is not included in the English edition.
