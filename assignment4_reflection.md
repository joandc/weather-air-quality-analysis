# Assignment 4 Reflection

## What worked well
- The holiday source integrated cleanly into the existing medallion pipeline.
- Creating `is_holiday` and `bad_air_day` added useful variables that expanded the analysis beyond the original weather-only comparisons.
- The final Gold dataset supported all five required analyses without needing major redesign.

## What was difficult
- Turning the app into a guided analytical story instead of just displaying charts and p-values.
- Matching each hypothesis test to the correct variables and explaining clearly why that method was appropriate.
- Refining the Streamlit design so that text, tables, legends, and filters were readable and visually consistent.

## Hardest assumptions to defend
- The t-tests assume that the sampling distribution of the mean is well-behaved, but PM2.5 and AQI can be right-skewed because of occasional pollution spikes.
- The chi-square test assumes sufficient expected cell counts, and that was harder to defend because the holiday subset is much smaller than the regular-day subset.
- The holiday flag is joined nationally by date and applied to both cities equally, which is practical for the assignment but may not reflect city-specific behavioral effects.

## What I would improve
- Use a longer date range so the tests are based on more observations and more seasonal variation.
- Add more cities to make the comparisons less narrow and more generalizable.
- Use provincial or city-specific holiday/event data instead of only a national holiday calendar.