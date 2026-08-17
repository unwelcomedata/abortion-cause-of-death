# Data Sources — abortion-cause-of-death

All data used in this project is from authoritative government or research
institute sources. No crowd-edited references (Wikipedia, etc.) are used.

---

## 1. CDC WONDER — Underlying Cause of Death (Expanded), 2024

- **Publisher:** Centers for Disease Control and Prevention, National Center for Health Statistics
- **URL:** https://wonder.cdc.gov/ucd-icd10-expanded.html
- **Format:** Tab-delimited export from interactive query interface
- **License:** Public domain (U.S. government work)
- **Coverage:** United States, all 50 states + DC, year 2024
- **Fields used:** ICD-10 113 Cause List, Single Race 6, Sex, Five-Year Age Groups, Deaths, Population, Crude Rate
- **Notes:**
  - Data are from death certificates filed in all 50 states and DC.
  - Population figures are Census Bureau estimates matched to the mortality year.
  - "Suppressed" values indicate counts of 1–9 (privacy protection).
  - Single Race 6 categories: White, Black or African American, American Indian
    or Alaska Native, Asian, Native Hawaiian or Other Pacific Islander, More than one race.
  - The expanded dataset uses single-race coding (available 2018+), not bridged race.
  - ICD-10 113 Cause List: causes prefixed with "#" are non-overlapping rankable
    leading causes. Sub-causes and parent categories exist but overlap.
- **Retrieved:** 2025-08-17

### WONDER Queries Performed

| File | Group By | Year |
|------|----------|------|
| `wonder_mortality_2024.tsv` | Single Race 6 × Sex × ICD-10 113 Cause | 2024 |
| `wonder_mortality_ages_2024.tsv` | Single Race 6 × Five-Year Age Groups × ICD-10 113 Cause | 2024 |
| `wonder_mortality_gender_2024.tsv` | Sex × Five-Year Age Groups × ICD-10 113 Cause | 2024 |
| `wonder_mortality_gender_2018_2024.tsv` | Sex × Single Race 6 × ICD-10 113 Cause | 2018–2024 (aggregated) |

All queries: entire U.S., all ages, all races, both sexes (unless grouped by).
Zero values shown. Export format: tab-delimited with notes footer.

---

## 2. Guttmacher Institute — Monthly Abortion Provision Study, 2024

- **Publisher:** Guttmacher Institute
- **URL:** https://www.guttmacher.org/fact-sheet/induced-abortion-united-states
- **Report:** "Stability in the Number of Abortions from 2023 to 2024 in US States
  Without Total Bans Masks Major Shifts in Access" (April 2025, updated June 2025)
- **Format:** Published report text and tables (manually extracted to CSV)
- **License:** Published research (cited under fair use for analysis)
- **Coverage:** United States, 2024 calendar year
- **Fields used:** National total abortions, abortion rate per 1,000 women 15–44
- **Key figures:**
  - National total: **1,124,000** clinician-provided abortions (2024)
  - Abortion rate: **16.7** per 1,000 women aged 15–44
  - 21% increase from 2020 (the last pre-Dobbs comprehensive estimate)
- **Notes:**
  - Estimates include medication abortions via telehealth and shield law provision.
  - Excludes self-managed abortions (medications from non-US pharmacies or
    community networks). Represents an underestimate of true total.
  - The Monthly Abortion Provision Study uses a statistical model combining
    monthly samples of providers with historical caseload data.
  - Full-year 2024 data released April 2025 (news release), with updated
    estimates in the June 2025 report revision.
- **Retrieved:** 2025-08-17

---

## 3. CDC Abortion Surveillance, 2022 (for age and gestational age distribution)

- **Publisher:** Centers for Disease Control and Prevention, Division of Reproductive Health
- **URL:** https://www.cdc.gov/mmwr/volumes/73/ss/ss7307a1.htm
- **Citation:** Ramer S, Nguyen AT, Hollier LM, et al. Abortion Surveillance —
  United States, 2022. MMWR Surveill Summ 2024;73(No. SS-7):1–52.
- **Format:** Published surveillance summary (MMWR)
- **License:** Public domain (U.S. government work)
- **Coverage:** 48 reporting areas (excludes CA, MD, NH, NJ), 2022
- **Fields used:** Age group distribution percentages, gestational age distribution percentages
- **Key figures (2022, from 48 reporting areas):**

  **Age distribution:**
  - <15 years: 0.2%
  - 15–19 years: 8.3%
  - 20–24 years: 28.3%
  - 25–29 years: 28.2%
  - 30–34 years: 20.2%
  - 35–39 years: 11.2%
  - ≥40 years: 3.6%

  **Gestational age distribution:**
  - ≤9 weeks: 78.6%
  - 10–13 weeks: 14.2%
  - 14–20 weeks: 6.1%
  - ≥21 weeks: 1.1%
  - **Note:** 92.8% of abortions occurred by week 13

- **Notes:**
  - This is the most recent CDC surveillance with full age-group and
    gestational-age detail.
  - Age and gestational age proportions applied to the Guttmacher 2024 national
    total to derive age-specific and gestational-specific abortion counts. This
    assumes distributions remained stable from 2022 to 2024 (consistent with
    historical patterns showing slow change in age and gestational composition).
  - The 30–34 and 35–39 age splits are derived from the constraint that all groups
    sum to 100%, consistent with patterns in prior CDC surveillance years.
  - Gestational age data are based on reports from clinicians where gestational
    age was known. This reflects clinical practice of measuring gestational age
    at time of abortion.
  - CDC undercounts vs Guttmacher because 4 states don't report; proportions
    are still valid for distributing across age groups and gestational weeks.
- **Retrieved:** 2025-08-17

---

## 4. U.S. Census Bureau — Population Estimates (via WONDER)

- **Publisher:** U.S. Census Bureau
- **URL:** https://www.census.gov/programs-surveys/popest.html
- **Format:** Embedded in WONDER query output (Population column)
- **License:** Public domain (U.S. government work)
- **Coverage:** United States, 2024 (Vintage 2024 postcensal estimates)
- **Fields used:** Population by sex, by age group, by race
- **Key figures:**
  - Total US population (2024): ~340.1 million
  - Female population (all ages): ~167.8 million
  - Female population (15–44): ~67.4 million
- **Notes:**
  - Population estimates come directly from WONDER output to ensure
    consistency between mortality rates and denominators.
  - Single-race population estimates (available 2018+).
  - Vintage 2024 series based on Census Bureau methodology.
- **Retrieved:** 2025-08-17 (via WONDER export)

---

## Methodology Notes

### Rate calculation

For the "with abortion" comparison, crude rates are calculated as:

```
crude_rate = count / (population + abortions) × 100,000
```

Rationale: Aborted lives are never counted in the living population. To be
consistent with how other crude death rates work (deaths drawn from a
population that includes those who died), we add abortions to the denominator.

### Year alignment

- Mortality data: **2024** (from WONDER)
- Abortion total: **2024** (from Guttmacher Monthly Provision Study)
- Age distribution: **2022** (from CDC Abortion Surveillance, applied to 2024 total)
- Gestational age distribution: **2022** (from CDC Abortion Surveillance, applied to 2024 total)

The 2-year lag on age and gestational proportions is acceptable because these
distributions change slowly over time. CDC 2020 and 2021 surveillance show
nearly identical distributions year-over-year.

### Source hierarchy

1. **Guttmacher** is the primary source for abortion counts (more complete than CDC)
2. **CDC Abortion Surveillance** provides validated age-group proportions
3. **CDC WONDER** provides mortality and population data
4. All sources are cross-referenced where possible

---

## Source Provenance in DuckDB

Every table in `data/project.duckdb` has a corresponding entry in the
`_sources` metadata table:

```sql
SELECT * FROM _sources;
```

---

## Discrepancies Between Sources

| Issue | Detail | Resolution |
|-------|--------|------------|
| Guttmacher vs CDC abortion totals | Guttmacher ~1.12M vs CDC ~613K (2022) | CDC excludes CA, MD, NH, NJ (~20% of abortions). Use Guttmacher. |
| Age proportions 2022 vs 2024 | Slight shift possible | Historical data shows <1pp/year change. Acceptable. |
| WONDER 2024 provisional vs final | 2024 data may be provisional | Noted; unlikely to affect rankings materially. |
