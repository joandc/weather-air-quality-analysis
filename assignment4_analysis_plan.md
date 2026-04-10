# Assignment 4 Analysis Plan

## 1. New source added

The new external source is the Nager.Date public holidays API for Canada.

- Endpoint used: `https://date.nager.at/api/v3/publicholidays/{year}/CA`
- Years pulled: `2024` and `2025`
- Bronze storage: `data/bronze/nager_holidays/`

The holiday API adds contextual information that was not present in the original weather and air quality sources. It makes it possible to test whether holiday dates are associated with air-quality patterns.

## 2. How the new source was cleaned

The raw holiday API responses are stored in Bronze as JSON snapshots.

In the Silver layer:

- the holiday payloads are read from Bronze
- `date`, `name`, and `global` are selected
- `name` is renamed to `holiday_name`
- `global` is renamed to `is_national`
- only national holidays are kept
- the cleaned result is saved to `data/silver/holidays_clean.csv`

## 3. Join key

The original weather and air-quality Silver tables are joined on:

- `date`
- `city`

The holiday source is then joined onto the Gold dataset by:

- `date`

This is a left join from Gold onto the holidays table. Because the holiday source is national, the same holiday date applies to both Toronto and Vancouver.

## 4. New variables created

- `is_holiday` (bool): `True` if the date is a Canadian statutory holiday
- `bad_air_day` (bool): `True` if `pm25_mean > 15`, using the WHO PM2.5 guideline

These variables expand the analysis beyond simple weather comparisons by creating a categorical holiday grouping and a categorical air-quality outcome.

## 5. Story / question

Main question:

How do weather conditions and holidays relate to air quality in Toronto and Vancouver, and which visible patterns are strong enough to support formal statistical testing?

## 6. Required analyses

1. One-sample t-test: Is mean daily AQI different from the benchmark value of 15?
2. Two-sample t-test: Do PM2.5 levels differ between rainy and non-rainy days?
3. Chi-square test: Is `bad_air_day` independent of `is_holiday`?
4. Levene's test: Is PM2.5 variability different on holidays versus regular days?
5. Pearson correlation: Is temperature associated with PM2.5 concentration?

## 7. Supporting chart for each analysis

1. One-sample t-test -> time-series chart of daily AQI with a benchmark line at 15
2. Two-sample t-test -> grouped boxplot of `pm25_mean` by `rainy_day`
3. Chi-square test -> stacked bar chart of `bad_air_day` counts by `is_holiday`
4. Levene's test -> grouped boxplot of `pm25_mean` by `is_holiday`
5. Pearson correlation -> scatterplot of `temp_max` versus `pm25_mean` with a trend line

## 8. Justification for each method

1. One-sample t-test:
   This test fits because it compares one sample mean, daily AQI, to one fixed benchmark value, 15.

2. Two-sample t-test:
   This test fits because `pm25_mean` is continuous and the comparison is between two independent groups: rainy days and non-rainy days.

3. Chi-square test:
   This test fits because both `bad_air_day` and `is_holiday` are categorical variables, so the question is about association between counts.

4. Levene's test:
   This test fits because the question is about whether PM2.5 spread or variance differs across two groups rather than whether the means differ.

5. Pearson correlation:
   This test fits because both temperature and PM2.5 are continuous variables, and the visual question is whether they show a linear relationship.

## 9. Important limitation to mention

The holiday source is joined by `date` only, not by `city`, so the same holiday flag is applied to both Toronto and Vancouver. This is reasonable for a national holiday source, but it may not capture city-specific or provincial differences in behavior.
