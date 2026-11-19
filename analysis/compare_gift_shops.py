import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from math import cos, hypot, radians

project = Path(__file__).resolve().parents[1]
candidates_path = project / "data" / "candidate_locations.csv"
output = project / "reports" / "candidate_gift_shops.csv"
radius_m = 300
endpoint = "https://overpass.private.coffee/api/interpreter"

with candidates_path.open(encoding="utf-8-sig", newline="") as file:
    candidates = list(csv.DictReader(file))

rows = []
latitudes = [float(candidate["latitude"]) for candidate in candidates]
longitudes = [float(candidate["longitude"]) for candidate in candidates]

# The margin around the outer points covers a 300 m radius in Turku.
margin = 0.006
south = min(latitudes) - margin
west = min(longitudes) - margin
north = max(latitudes) + margin
east = max(longitudes) + margin

query = f'''
    [out:json][timeout:25];
    nwr["shop"="gift"]({south},{west},{north},{east});
    out center;
'''
url = f"{endpoint}?{urlencode({'data': query})}"

with urlopen(url, timeout=90) as response:
    result = json.load(response)

if result.get("remark"):
    raise RuntimeError(result["remark"])

retrieved_at = datetime.now(UTC).isoformat(timespec="seconds")
rows = []
for candidate, latitude, longitude in zip(candidates, latitudes, longitudes, strict=True):
    names = []
    for shop in result["elements"]:
        point = shop.get("center", shop)
        north_m = (point["lat"] - latitude) * 111_195
        east_m = (point["lon"] - longitude) * 111_195 * cos(radians(latitude))
        if hypot(north_m, east_m) <= radius_m:
            names.append(shop["tags"].get("name", "(unnamed)"))

    candidate_id = candidate["candidate_id"]
    rows.append([candidate_id, candidate["name"], radius_m, len(names), retrieved_at])
    print(f"{candidate_id}: {len(names)} — {', '.join(names) or 'none found'}")

output.parent.mkdir(exist_ok=True)
with output.open("w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["candidate_id", "name", "radius_m", "osm_gift_shop_count", "retrieved_at_utc"])
    writer.writerows(rows)

print(f"Saved {output.name}")
