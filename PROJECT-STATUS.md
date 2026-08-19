# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-19
**Status:** IN PROGRESS — Trend line chart updated to rates. Next: bar chart race + historical data.

---

## Current Phase: Exploratory Viz Iteration (04-viz.ipynb)

### Recent Work (This Session)

- **Trend line chart overhauled** in `04-viz.ipynb`:
  - Changed from static top-5-by-cumulative to **dynamic top-5-per-year** ranking
  - Switched from raw death counts to **crude rate per 100,000 population**
  - Lines break when a cause drops out of the top 5 for that year (contiguous segments)
  - Abortion rate computed using same total population denominator for comparability
  - Key finding: on a rate basis, abortion (~330/100k in 2024) would rank **#1**, above heart disease (201/100k)
  - Output: `outputs/trend_top5_rate_plus_abortion.png`

- **Investigated extending data pre-1999:**
  - Current mortality data is ICD-10 (1999-2024 via WONDER)
  - Pre-1999 requires ICD-9 Compressed Mortality File (1979-1998)
  - CDC WONDER query interface kept timing out — revisit later
  - Top 5 causes are broadly stable across ICD revisions (heart, cancer, stroke, accidents, respiratory)
  - Abortion peaked ~430/100k in early 1980s, roughly crossing heart disease rate at that time

---

## Social Charts (04b-viz-social.ipynb) — COMPLETE

1. **Chart 1: Female vs Male top 10 (per 100k)** — DONE
2. **Chart 1b: White vs Black top 10 (per 100k)** — DONE
3. **Chart 2: National Abortion Comparison** — DONE
4. **Charts 3 & 4: Abortion by Race (White & Black)** — DONE

---

## Next Steps (If Reopening)

### Priority: Bar Chart Race

- [ ] Build a **bar chart race** (animated ranking chart) showing top causes of death + abortion over time
- [ ] Need a reusable bar chart race template (consider `bar_chart_race` Python package or custom matplotlib animation)
- [ ] Data: combine 1999-2024 ICD-10 rates + abortion rates from Guttmacher
- [ ] If extending to 1973+: pull ICD-9 data from CDC Compressed Mortality (1979-1998) when WONDER cooperates
- [ ] Guttmacher abortion data available 1973-2024 — rate peaks ~430/100k around 1980-81

### Historical Data Pull

- [ ] CDC WONDER Compressed Mortality 1979-1998 (ICD-9): http://wonder.cdc.gov/cmf-icd9.html
  - Query: national level, all ages, all races, by year, top cause categories
  - Was timing out during this session — try again later or use CDC Health United States Table 005 (PDF/Excel with selected years back to 1950)
- [ ] Stitch pre-1999 and post-1999 data with note about ICD-9→10 boundary

### Other Ideas

- [ ] Social posting plan (copy, alt text, thread strategy)
- [ ] Additional charts: Alzheimer's disparity, diabetes/kidney cluster, accidents by sex x race

---

## Key Design Decisions

- **Per-capita rates** for trend comparisons (controls for 22% population growth 1999-2024)
- **Crude rate per 100k** (not age-adjusted) for the trend chart — matches WONDER output directly
- **Dynamic ranking per year** — shows COVID-19 entering/leaving top 5 naturally
- **Abortion uses total population denominator** for comparability with all-cause mortality rates

---

## Environment

- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13)
- DuckDB: `data/project.duckdb`
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch)
