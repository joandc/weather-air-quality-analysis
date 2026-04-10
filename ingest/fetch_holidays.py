import json
from datetime import datetime
from pathlib import Path
import requests

# Nager.Date Public Holidays API — no API key required
NAGER_URL = "https://date.nager.at/api/v3/publicholidays"

# Country code for Canada
COUNTRY_CODE = "CA"

# Match the same years as your weather/air quality data
YEARS = [2024, 2025]

# Bronze output folder — keeps raw API responses exactly as returned
HOLIDAYS_BRONZE_DIR = Path("data/bronze/nager_holidays")
HOLIDAYS_BRONZE_DIR.mkdir(parents=True, exist_ok=True)

# One timestamp per run (same pattern as run_ingestion.py)
timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

for year in YEARS:
    url = f"{NAGER_URL}/{year}/{COUNTRY_CODE}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Save raw JSON exactly as returned — Bronze layer
    output_file = HOLIDAYS_BRONZE_DIR / f"canada_holidays_{year}_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved Bronze holiday snapshot for {year} — {len(data)} holidays")
