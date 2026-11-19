import csv
from math import ceil
from pathlib import Path

project = Path(__file__).resolve().parents[1]
listings = project / "data" / "rent_listings.csv"

with listings.open(encoding="utf-8-sig", newline="") as file:
    listing = next(row for row in csv.DictReader(file) if row["listing_id"] == "KIR01")

rent = float(listing["asking_rent_eur_month"])

# Scenario assumptions; monetary values are in EUR.
open_days = 26
average_purchase_excl_vat = 18
variable_cost_per_purchase = 10
monthly_staff_cost = 1800
other_monthly_fixed_costs = 300

contribution_per_purchase = average_purchase_excl_vat - variable_cost_per_purchase
monthly_fixed_costs = rent + monthly_staff_cost + other_monthly_fixed_costs
purchases_per_month = ceil(monthly_fixed_costs / contribution_per_purchase)
purchases_per_day = ceil(purchases_per_month / open_days)

print(f"Premises: {listing['address']}")
print(f"Scenario monthly fixed costs: {monthly_fixed_costs:,.0f} EUR")
print(f"Contribution after variable costs: {contribution_per_purchase:.0f} EUR per purchase")
print(f"Break-even threshold: {purchases_per_month} purchases per month, approximately {purchases_per_day} per working day")
print("\nSensitivity to contribution per purchase:")
for amount in (6, 8, 10):
    monthly = ceil(monthly_fixed_costs / amount)
    daily = ceil(monthly / open_days)
    print(f"{amount} EUR per purchase — {monthly} per month, {daily} per working day")

print("\nRequired footfall at the entrance (scenario only):")
for conversion_percent in (1, 2, 3):
    passages = ceil(purchases_per_day / (conversion_percent / 100))
    print(f"{conversion_percent}% of passages convert to a purchase: {passages} passages per day")
