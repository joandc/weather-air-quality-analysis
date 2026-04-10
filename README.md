# Weather Air Quality Analysis

Medallion data pipeline and Streamlit dashboard analyzing weather and air quality patterns in Toronto and Vancouver, enriched with Canadian holiday data.

## Overview

This repository contains Assignment 4, which serves as Part 2 of the Assignment 3 weather and air quality analytics project. It combines:

- a medallion-style pipeline with Bronze, Silver, and Gold layers
- daily weather and air-quality data from Open-Meteo
- a Canadian public holiday source from the Nager.Date API
- a Streamlit app that presents the analysis as a guided statistical story

The project starts with raw source data, cleans and joins it into a Gold dataset, and then uses that dataset in a Streamlit app to move from context, to visuals, to formal hypothesis testing, and finally to reflection and limitations.

## Main Question

How do weather conditions and holidays relate to air quality in Toronto and Vancouver, and which visible patterns are strong enough to support formal statistical testing?

## Data Sources

This project uses three external data sources:

- Open-Meteo Historical Weather
- Open-Meteo Air Quality
- Nager.Date public holidays API for Canada

The weather and air-quality data are collected for:

- Toronto
- Vancouver

The holiday source adds contextual information that was not available in the original Assignment 3 pipeline.

## Pipeline Design

### Bronze

Raw source responses are stored exactly as returned:

- `data/bronze/open_meteo_weather/`
- `data/bronze/open_meteo_air_quality/`
- `data/bronze/nager_holidays/`

Each Bronze file is timestamped so snapshots can be retained.

### Silver

The Silver layer stores cleaned, analysis-ready source tables:

- `data/silver/weather_daily_clean.csv`
- `data/silver/air_quality_daily_clean.csv`
- `data/silver/holidays_clean.csv`

At this stage:

- weather data is flattened into daily records
- hourly air-quality data is aggregated into daily measures
- holiday API data is filtered to national holidays and standardized by date

### Gold

The Gold dataset is:

- `data/gold/weather_air_quality_daily.csv`

The Gold build:

- joins weather and air quality on `date` and `city`
- uses an inner join for the core weather/air-quality merge
- joins the holiday source by `date`
- fills non-holiday dates as `False`
- keeps only the fields needed for analysis and the Streamlit app

## Derived Variables

The final Gold dataset includes these derived features:

- `rainy_day`: `True` when daily precipitation is greater than 0
- `is_holiday`: `True` when the date is a Canadian statutory holiday
- `bad_air_day`: `True` when `pm25_mean > 15`, based on the WHO PM2.5 guideline

These variables make it possible to test both weather-based and holiday-based questions.

## Assignment 4 Analysis

The Streamlit app supports five required analyses:

1. One-sample t-test: Is mean daily AQI different from the benchmark value of 15?
2. Two-sample t-test: Do PM2.5 levels differ between rainy and non-rainy days?
3. Chi-square test: Is `bad_air_day` independent of `is_holiday`?
4. Levene's test: Is PM2.5 variability different on holidays versus regular days?
5. Pearson correlation: Is temperature associated with PM2.5 concentration?

Each test is supported by a chart that motivates the formal method used in the app.

## Streamlit App

The main Assignment 4 app is:

- `app/streamlit_app.py`

The app is organized as a guided analytical story with these sections:

- Project overview and data story
- Data foundations
- Visual evidence
- Formal hypothesis tests
- Reflection and limitations

It also includes:

- city and date filters in the sidebar
- chart captions that connect visual evidence to hypothesis tests
- plain-language interpretations of each statistical result
- a branded hero section using the AtmoScope logo

## Repository Layout

```text
.
|-- README.md
|-- assignment4_analysis_plan.md
|-- assignment4_reflection.md
|-- pyproject.toml
|-- data/
|   |-- bronze/
|   |   |-- open_meteo_weather/
|   |   |-- open_meteo_air_quality/
|   |   `-- nager_holidays/
|   |-- silver/
|   `-- gold/
|-- ingest/
|   `-- fetch_holidays.py
|-- transform/
|   |-- build_silver.py
|   `-- build_gold.py
`-- app/
    |-- streamlit_app.py
    `-- assets/
```

## How To Run

### 1. Install dependencies

Using `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
pip install -r requirements.txt
```

### 2. Build or refresh the pipeline

Run the ingestion and transform steps:

```bash
uv run python ingest/run_ingestion.py
uv run python ingest/fetch_holidays.py
uv run python transform/build_silver.py
uv run python transform/build_gold.py
```

### 3. Launch the Streamlit app

```bash
uv run streamlit run app/streamlit_app3.py
```

## Join and Data Notes

- Weather and air quality are joined on `date` and `city`.
- The holiday source is joined on `date` only because it is a national calendar.
- The holiday flag therefore applies to both cities on the same date.
- Missing hourly air-quality values are handled during daily aggregation where possible.
- The Gold dataset drops rows missing required analysis fields.

## Limitations

Important limitations in this project include:

- the holiday source is national rather than city-specific
- holiday observations are much fewer than regular days
- AQI and PM2.5 can be skewed by occasional spikes
- statistical significance does not imply practical importance or causation

## Supporting Docs

- `assignment4_analysis_plan.md`: analysis design and method justification
- `assignment4_reflection.md`: reflection on what worked, what was difficult, assumptions, and improvements

## AI Usage

AI tools used:

- ChatGPT / Codex

AI was used under my prompting direction for:

- assignment planning
- refining the data pipeline and supporting code
- documentation refinement
- streamlining the Streamlit app design, layout, and narrative structure

AI-generated contributions and executions were guided by my prompts, review decisions, and design choices throughout the project.

All implementation details, joins, derived variables, and analysis choices were checked against the actual repository contents and assignment requirements.
