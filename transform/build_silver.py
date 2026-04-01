# Import libraries
import json
from pathlib import Path
import pandas as pd

# Define Bronze and Silver paths
WEATHER_BRONZE_DIR = Path("data/bronze/open_meteo_weather")
AIR_QUALITY_BRONZE_DIR = Path("data/bronze/open_meteo_air_quality")

WEATHER_SILVER_PATH = Path("data/silver/weather_daily_clean.csv")
AIR_QUALITY_SILVER_PATH = Path("data/silver/air_quality_daily_clean.csv")

# Define the cities: the same cities as from the ingestion script
CITIES = [
    {"name": "Toronto", "slug": "toronto"},
    {"name": "Vancouver", "slug": "vancouver"},
]


# Read the latest Bronze file for each city
# helper function
def latest_file(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No files found for {pattern}")
    return matches[-1]


weather_frames = []
air_quality_frames = []

for city in CITIES:
    weather_path = latest_file(WEATHER_BRONZE_DIR, f"{city['slug']}_weather_*.json")
    # Load a Bronze JSON file
    with open(weather_path, "r", encoding="utf-8") as f:
        weather_payload = json.load(f)

    # The weather API already gives daily values, so it can be flatten directly into a DataFrame.
    # Use the `daily` section of the payload:

    daily = weather_payload["daily"]
    weather_df = pd.DataFrame(
        {
            "date": pd.to_datetime(daily["time"]).date,
            "city": city["name"],
            "temp_max": pd.to_numeric(daily["temperature_2m_max"], errors="coerce"),
            "temp_min": pd.to_numeric(daily["temperature_2m_min"], errors="coerce"),
            "precipitation_sum": pd.to_numeric(
                daily["precipitation_sum"], errors="coerce"
            ),
        }
    )
    # append  cleaned city DataFrame to the designated list
    weather_frames.append(weather_df)

    # Do the same for air_quality
    air_quality_path = latest_file(
        AIR_QUALITY_BRONZE_DIR, f"{city['slug']}_air_quality_*.json"
    )
    with open(air_quality_path, "r", encoding="utf-8") as f:
        air_quality_payload = json.load(f)

    # The air-quality API gives hourly arrays, so first create an hourly DataFrame:
    hourly = air_quality_payload["hourly"]
    air_quality_df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(hourly["time"]),
            "city": city["name"],
            "pm25": pd.to_numeric(hourly["pm2_5"], errors="coerce"),
            "pm10": pd.to_numeric(hourly["pm10"], errors="coerce"),
            "aqi": pd.to_numeric(hourly["us_aqi"], errors="coerce"),
        }
    )
    # Then create a `date` column:
    air_quality_df["date"] = air_quality_df["timestamp"].dt.date

    # Aggregate hourly air quality to daily values
    # Group by `date` and `city`: This gives you a daily Silver table from hourly Bronze data.
    daily_air_quality = air_quality_df.groupby(["date", "city"], as_index=False).agg(
        pm25_mean=("pm25", "mean"),
        pm10_mean=("pm10", "mean"),
        aqi_max=("aqi", "max"),
    )
    air_quality_frames.append(daily_air_quality)

# Combine the city DataFrames after the loop
weather_silver = pd.concat(weather_frames, ignore_index=True).sort_values(
    ["city", "date"]
)
air_quality_silver = pd.concat(air_quality_frames, ignore_index=True).sort_values(
    ["city", "date"]
)

# Check for output folder
WEATHER_SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)
# Save the files
weather_silver.to_csv(WEATHER_SILVER_PATH, index=False)
air_quality_silver.to_csv(AIR_QUALITY_SILVER_PATH, index=False)

# Add print statements to check if the files were created:
print(f"Saved {WEATHER_SILVER_PATH}")
print(f"Saved {AIR_QUALITY_SILVER_PATH}")
