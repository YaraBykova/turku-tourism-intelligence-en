# Optional souvenir-store break-even scenario

This is separate from the main DA/DE analysis. It does not select a store site or estimate actual sales.

The recorded listing `KIR01` is Linnankatu 9–11, 49.5 m², asking rent EUR 1,372/month. Electricity and water are charged by consumption; VAT treatment is unknown in the recorded data. Listing observed on 16 November 2026: [source](https://tuloskiinteistot.fi/fi/17152/turku/linnankatu-9-11/). Availability and terms must be checked again before any real decision.

Scenario assumptions: 26 working days/month, EUR 1,800 staffing, EUR 300 other fixed costs, and EUR 8 contribution per purchase after variable costs. Fixed monthly costs are EUR 3,472. The threshold is 434 purchases/month, or 17 per working day after rounding up.

If 1%, 2% or 3% of passages convert to purchases, the corresponding rounded daily passage thresholds are 1,700, 850 and 567. These are hypothetical requirements, not measured footfall. A city counter cannot be treated as traffic at a particular shop entrance.

```powershell
py -3.14 analysis/break_even.py
```

`listing_id=KIR01` is not mapped to candidate points T01–T03. The supplementary `analysis/compare_gift_shops.py` queries OpenStreetMap gift-shop tags within 300 m of those points. It is outside the scheduled hotel-night pipeline and does not establish complete competitor coverage or actual demand. It makes a live external request and requires a separate source review before use in a business decision.

The scenario covers only included operating costs. It is not a full investment appraisal or evidence that a store would be profitable.
