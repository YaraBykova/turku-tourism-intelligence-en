# Power BI guide

Open `turku_tourism_dashboard.pbip` from the English folder. Keep the neighbouring `.Report` and `.SemanticModel` folders. This distribution contains no old PBIX, local settings or imported cache.

## Connection and refresh

Source: PostgreSQL `127.0.0.1:5433`, database `turku_bi`, view `marts.tourism_seasonality`, user `turku`. Enter your local database password in Power BI if prompted. Credentials are not part of the report definitions.

Select **Refresh** after opening to import all 279 rows and process the calculated labels/calendar. The English report can read the database already running for the Russian project. A separate English Docker stack is unnecessary for that use. The model uses `en-GB` culture; the installed application's own interface language is independent of the report captions.

Airflow refreshes the database, while Power BI import must be refreshed separately. Markdown analysis is a dated snapshot. There is no Power BI Service publication or automatic local import refresh.

## Pages

1. **01 · Overview:** Turku hotel nights, segment volumes, international share, matched prior-year changes and monthly charts. Default year: 2026.
2. **02 · Seasonality:** complete years only; domestic/international shares of their respective annual totals. Default year: 2025.
3. **03 · City comparison:** three growth cards, a seven-column table, domestic/international contributions to growth and annual city profiles. Default year: 2026; profile year: 2025 until 2026 is complete.

All pages are 1600 × 1000. The first two retain Turku page filters; there is no report-wide Turku filter. Chart selections do not silently alter the other visuals' comparison periods. Year slicers control the intended year.

## Calculations

31 measures retain their original English identifiers. Translated strings change labels, month names and units only. `City` maps the three municipality codes to English names. `Profile Months` is a disconnected 12-row calendar so an incomplete year cannot truncate the full-year profile axis.

Prior-year measures preserve the selected municipalities and use the current context's observed month numbers. All required prior months must be present. 2019 has no 2018 baseline, so changes are blank.

Segment contribution, pp = (segment current nights − segment prior nights) / prior total nights × 100. Domestic and international contributions sum to total growth before rounding. A segment's own growth rate uses its own prior denominator instead.

## Check values

| Context | Expected |
|---|---:|
| Overview 2026, total | 689,463 |
| Domestic / international | 560,859 / 128,604 |
| International share | 18.65% |
| Total / domestic / international growth | +6.66% / +3.96% / +20.28% |
| International share change | +2.11 pp |
| Overview 2025, full-year total | 822,620 |
| Seasonality 2025, peak | July |
| Domestic / international summer shares | 35.36% / 38.94% |
| City growth 2026: Turku / Tampere / Oulu | +6.66% / +0.49% / +13.40% |
| City nights 2026: Turku / Tampere / Oulu | 689,463 / 1,023,197 / 449,842 |
| City growth 2025: Turku / Tampere / Oulu | +0.26% / +1.55% / −0.34% |

For either selected 2025 or incomplete 2026, the city profile currently uses complete 2025. Each city's 12 monthly shares should sum to 100%. The profile caption must show the actual year.

The original Russian report's calculations and corrected layout were verified, including a user-provided image of the three-city page. That visual confirmation does not establish the English text layout: open this English PBIP and check labels, table columns, legends and footer after refresh. See [verification](verification.md) for the English edition's automated checks.

## Interpretation

Hotel nights do not measure unique tourists, entrance-level footfall or sales. 2026 data are preliminary; the 2025 classification change limits earlier comparisons. Oulu's official EU title European Capital of Culture 2026 is context; its causal effect is not estimated. Source: Statistics Finland, CC BY 4.0.

## English report locale and user-provided visual confirmation

The user opened the English edition and supplied images of all three pages: English captions and month names are visible, check values match, the comparison table contains all seven columns and three cities, and the 12-month 2025 profiles are displayed under selected 2026. These are user-provided images, not screenshots created by the agent. They also showed Russian auto-unit labels and decimal commas inherited from the viewer environment.

The English model already used en-GB. The report now explicitly sets `settings.locale` to `en-GB` as well, validated against the official report schema. Numeric measures, values, filters and page geometry were not changed. See [Microsoft's report format-string locale documentation](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-default-format-string-locale). Close the old open report without saving over the file correction, reopen the same English PBIP, and check decimal separators and auto-unit labels. This last formatting correction has not yet been confirmed visually.

## Count-axis display units

After the report-locale correction, the user confirmed English number formatting on the seasonality page (822,620 and 35.36% / 38.94%). Automatic chart-unit abbreviations still appeared in Russian. The three count axes on Overview and Seasonality now explicitly use Display units = None and zero decimal places, showing full values such as 50,000 and 100,000. Percentage/profile/contribution axes, query bindings, calculations and visual positions are unchanged. The corrected definitions passed the official visual schema. Reopening the English PBIP is required; the latest axis correction is pending user confirmation.

## Final published PDF status

The final English and Russian PDFs have each been reviewed across all three pages. Both use Overview 2026, Seasonality 2025, and City comparison 2026 with a labelled 2025 seasonal profile. Values and tables match the validated snapshot. English decimal points, thousands separators and full count-axis values have been confirmed; the earlier pending formatting notes above record the implementation history.
