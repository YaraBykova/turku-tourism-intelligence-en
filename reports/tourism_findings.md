# Hotel nights in Turku: seasonality and change

Original analysis: 18 November 2026. On 19 November it was extended to [Turku, Tampere and Oulu](city_comparison.md). The Turku metrics below were reconciled with the fresh extract and remained unchanged.

Source: Statistics Finland, StatFin 11lm, CC BY 4.0. The analysis uses 93 months, January 2019–September 2026.

## Analytical questions

1. How concentrated is hotel demand in summer?
2. How did hotel nights change in the latest available year?
3. How much did domestic and international nights contribute?

## Seasonality

In every complete year from 2019 to 2025, hotel nights peaked in July.

In 2025, June–August accounted for **35.92% of annual hotel nights** and July alone for **14.89%**. The other nine months accounted for **64.08%**: the summer peak is pronounced, but a substantial share of nights occurs in other seasons.

## Changes over matched periods

January–September 2026 recorded **689,463 hotel nights**, compared with **646,423** in January–September 2025.

The increase was **43,040 nights, or 6.66%**.

Growth occurred in seven of the nine months. January had the largest absolute increase: **+12,121 nights**. April and May together declined by **6,832 nights**.

## Segment changes

| Metric | Domestic nights | International nights |
|---|---:|---:|
| January–September 2025 | 539,505 | 106,918 |
| January–September 2026 | 560,859 | 128,604 |
| Absolute change | +21,354 | +21,686 |
| Change, % | +3.96% | +20.28% |

Both segments made almost equal absolute contributions to the overall increase. International nights grew faster from a smaller initial base.

The international share rose from **16.54% to 18.65%**, an increase of **2.11 percentage points**.

## Segment seasonality

In 2025, both domestic and international nights peaked in July.

June–August accounted for **35.36% of annual domestic nights** and **38.94% of annual international nights**. The international segment was somewhat more concentrated in summer.

The difference was particularly visible in August: it accounted for **13.42% of annual international nights**, compared with **9.67% of domestic nights**.

Shares are calculated separately using each segment's annual total. This finding applies to 2025; the stability of this profile across other years has not been checked.

## Calculation method

The comparison uses the same calendar months. The international share is calculated from summed international and total nights over the entire period.

Segment growth:

```text
(2026 nights / 2025 nights − 1) × 100%
```

The calculations can be reproduced with these SQL queries:

- `tourism_summary.sql`;
- `tourism_same_period.sql`;
- `tourism_monthly_change.sql`;
- `tourism_segments_same_period.sql`;
- `tourism_segment_seasonality.sql`.

## Limitations

Data for 2026 are preliminary and may be revised. The 2025 hotel-classification change limits comparability with earlier years.

Hotel nights are not unique tourists, pedestrian footfall or souvenir sales. This analysis does not establish the causes of changes or the profitability of a particular shop.
