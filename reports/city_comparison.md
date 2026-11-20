# Turku, Tampere and Oulu: hotel-night growth and seasonality

Analysis snapshot: 19 November 2026. All numerical comparisons use Statistics Finland StatFin 11lm. This is descriptive analysis.

## Question and purpose

How have hotel nights in Turku changed relative to Tampere and Oulu, and what have domestic and international nights contributed?

The comparison puts one city's changes in the context of a small group of other cities and describes seasonal concentration. It provides context for planning seasonal tourism services.

## Why these cities

The fixed group is Turku `853`, Tampere `837` and Oulu `564`, three large cities outside the capital region. The units are municipalities, not metropolitan areas or tourism regions. [Turku's 2026 operating-environment review, page 27](https://www.turku.fi/sites/default/files/document/muutoksen-tuulet-toimintaymparistokatsaus-2026-1.pdf) includes Tampere and Oulu among its tourism comparison cities outside the capital region. The group was chosen before calculating its growth rates. This rationale does not establish identical markets.

The review's accommodation totals are not mixed into our metrics: all counts here are hotel nights from 11lm. Volumes are not normalised by population or hotel capacity; larger volume does not imply greater efficiency.

## Same periods: January–September 2026 versus January–September 2025

| City | 2025 nights | 2026 nights | Absolute change | Growth | International share, 2026 |
|---|---:|---:|---:|---:|---:|
| Turku | 646,423 | 689,463 | +43,040 | +6.66% | 18.65% |
| Tampere | 1,018,180 | 1,023,197 | +5,017 | +0.49% | 13.91% |
| Oulu | 396,702 | 449,842 | +53,140 | +13.40% | 17.85% |

Turku's growth exceeded Tampere's by 6.17 percentage points and trailed Oulu's by 6.74 points. Tampere retained the largest absolute volume. These comparisons do not explain the causes or assess management performance.

## Segment contributions

| City | Domestic change | International change | Domestic contribution, pp | International contribution, pp |
|---|---:|---:|---:|---:|
| Turku | +21,354 | +21,686 | +3.30 | +3.35 |
| Tampere | +3,968 | +1,049 | +0.39 | +0.10 |
| Oulu | +39,467 | +13,673 | +9.95 | +3.45 |

Contribution = segment change / previous-period total nights × 100. The two contributions sum to total percentage growth before rounding. A segment's own growth rate instead divides by that segment's previous-period nights.

Turku's two segments contributed almost equally in absolute terms. Most of Oulu's increase came from domestic nights (+39,467 of +53,140). Both segments in Tampere grew little relative to their respective baselines. International nights grew 20.28% in Turku, 20.53% in Oulu and 0.74% in Tampere, so Turku's international growth was not unique within this group.

International share increased by 2.11 pp in Turku, 1.06 pp in Oulu and 0.03 pp in Tampere.

## Summer concentration: complete 2025

| City | Annual nights | June–August: total | Domestic summer share | International summer share | Peak total month |
|---|---:|---:|---:|---:|---|
| Turku | 822,620 | 35.92% | 35.36% | 38.94% | July |
| Tampere | 1,333,325 | 32.09% | 30.95% | 39.38% | July |
| Oulu | 521,194 | 29.45% | 29.70% | 28.27% | July |

Turku was more summer-concentrated in total and domestic nights. Its international summer share was close to Tampere's, while Oulu's was lower. All three total-night series peaked in July. One full year's profile is not a forecast or evidence that future years must follow it.

On the city-profile chart, each month is divided by that city's own full-year total; its 12 shares sum to 100%. The separate Turku seasonality page normalises domestic and international segments independently.

## Practical interpretation

Turku's increase was supported by both segments. Its position between Tampere and Oulu limits a claim that Turku was exceptionally fast-growing. Its higher summer concentration is relevant context when planning seasonal tourism services; however, 64.08% of Turku's 2025 hotel nights occurred outside June–August.

## Reproduction and data contract

- Source: [StatFin 11lm](https://pxdata.stat.fi/PXWeb/pxweb/en/StatFin/StatFin__matk/11lm.px), [API](https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/matk/11lm.px), Statistics Finland, CC BY 4.0.
- Unit: hotel night; grain: municipality × calendar month. `yopyneet`, `yopyneet_fi`, `yopyneet_ul` correspond to total, domestic and international nights.
- Example three-city source snapshot: `data/raw/statfin/11lm_20261118T225838_840380Z.json`, retrieved 18 November 2026 at 22:58:38 UTC (19 November at 01:58:38 Europe/Moscow). Raw query, metadata and response are preserved.
- `data/hotel_nights_monthly.csv`: 279 rows, January 2019–September 2026, 93 months per city with identical coverage. Missing or suppressed values are not replaced with zero.
- `marts.tourism_city_comparison`: municipality/year totals and matched prior-year months. Missing prior baselines produce NULL; 2019 has no 2018 baseline in this project.
- `sql/tourism_city_comparison.sql` selects the latest available year; `sql/tourism_city_seasonality.sql` selects the latest common full year.
- `dbt build` refreshes the comparison mart alongside the other models; Airflow retains seven tasks and the 01:20 Europe/Moscow schedule.
- The third Power BI page uses the selected year for growth and that year for seasonality when complete, otherwise the preceding full year. The actual profile year is labelled explicitly. The seasonal axis uses a separate 12-month calendar.
- This Markdown file is a dated analytical snapshot. It is not rewritten automatically on refresh; SQL views and refreshed Power BI import use updated data.

## Limits

2026 data are preliminary. [The 2025 hotel-classification change](https://stat.fi/en/documentation/changes-in-statistics/cmj86bfdy90vs07uk47jbqm2i) limits comparisons with earlier years; the main comparison is 2026 versus 2025.

[Oulu is a European Capital of Culture in 2026](https://oulu2026.eu/en/welcome-to-oulu2026/). This provides context rather than an established cause of growth. Event effects, capacity, prices, business travel and other influences are not estimated. Nights reflect available supply as well as demand, and this analysis does not measure unmet demand.

Two comparison cities do not support generalisation to all Finland. Results are not a causal explanation or forecast.
