from pathlib import Path
import pandas as pd

# Define Silver input paths and Gold output path
WEATHER_SILVER_PATH = Path("data/silver/weather_daily_clean.csv")
AIR_QUALITY_SILVER_PATH = Path("data/silver/air_quality_daily_clean.csv")
GOLD_PATH = Path("data/gold/weather_air_quality_daily.csv")

# Read the Silver files
weather = pd.read_csv(WEATHER_SILVER_PATH, parse_dates=["date"])
air_quality = pd.read_csv(AIR_QUALITY_SILVER_PATH, parse_dates=["date"])

# Join the Silver tables on `date` and `city`
# inner join is used to only keep rows where both sources exist for the same day
# and city.
gold = weather.merge(air_quality, on=["date", "city"], how="inner")
gold = gold.sort_values(["city", "date"]).reset_index(drop=True)

# Add `rainy_day` as the key derived column for Part 2 questions
gold["rainy_day"] = gold["precipitation_sum"].fillna(0).gt(0)

# Drop rows missing key values
gold = gold.dropna(subset=["aqi_max", "pm25_mean", "precipitation_sum"])

# Select the final Gold columns
gold = gold[
    [
        "date",
        "city",
        "temp_max",
        "temp_min",
        "precipitation_sum",
        "pm25_mean",
        "pm10_mean",
        "aqi_max",
        "rainy_day",
    ]
]

# --- Assignment 4 additions ---

# Load holidays from Silver
HOLIDAYS_SILVER_PATH = Path("data/silver/holidays_clean.csv")
holidays = pd.read_csv(HOLIDAYS_SILVER_PATH, parse_dates=["date"])
holidays["is_holiday"] = True

# Join holidays onto gold by date only
gold = gold.merge(holidays[["date", "is_holiday"]], on="date", how="left")
gold["is_holiday"] = gold["is_holiday"].fillna(False)

# Add bad_air_day: True if pm25_mean is above WHO guideline of 15 µg/m³
gold["bad_air_day"] = gold["pm25_mean"] > 15

# Update column selection to include new columns
gold = gold[
    [
        "date",
        "city",
        "temp_max",
        "temp_min",
        "precipitation_sum",
        "pm25_mean",
        "pm10_mean",
        "aqi_max",
        "rainy_day",
        "is_holiday",
        "bad_air_day",
    ]
]

# Save the Gold CSV
GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)
gold.to_csv(GOLD_PATH, index=False)
print(f"Saved {GOLD_PATH}")
