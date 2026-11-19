# Turku hotel nights: volume, change and segment seasonality

Original analysis: 18 November 2026; checked again during the three-city extension on 19 November. Source: Statistics Finland, StatFin 11lm, CC BY 4.0. There are 93 monthly Turku observations, January 2019–September 2026. See the [three-city comparison](city_comparison.md) for the main comparative question.

## Findings

- July was the peak total-night month in every complete year from 2019 to 2025.
- In 2025, June–August represented 35.92% of total nights and July alone 14.89%; the other nine months accounted for 64.08%.
- January–September 2026 had 689,463 nights versus 646,423 in the same months of 2025: +43,040, or +6.66%.
- Growth occurred in seven of nine months. January had the largest absolute increase, +12,121; April and May together declined by 6,832.

| Metric | Domestic | International |
|---|---:|---:|
| January–September 2025 | 539,505 | 106,918 |
| January–September 2026 | 560,859 | 128,604 |
| Change | +21,354 | +21,686 |
| Growth | +3.96% | +20.28% |

The segments made almost equal absolute contributions. International nights grew faster from a smaller base; their combined-period share rose from 16.54% to 18.65%, a 2.11 pp increase.

## Segment seasonality in complete 2025

Both segments peaked in July. June–August accounted for 35.36% of domestic nights and 38.94% of international nights. August represented 9.67% of annual domestic nights versus 13.42% of international nights. Shares use each segment's own annual total, not the combined total. Stability across future years is not established by this one-year profile.

## Method and SQL

Growth = (current nights / same-period prior-year nights − 1) × 100%. International share is the ratio of period sums, not the average of monthly shares. Only full 12-month years are used for annual profiles.

Queries: `sql/tourism_summary.sql`, `sql/tourism_same_period.sql`, `sql/tourism_monthly_change.sql`, `sql/tourism_segments_same_period.sql` and `sql/tourism_segment_seasonality.sql`.

2026 values are preliminary. Hotel classification changed in 2025, limiting earlier-year comparisons. Hotel nights are not unique tourists, store footfall or sales. No causal explanation, forecast or store-profit estimate is established.
