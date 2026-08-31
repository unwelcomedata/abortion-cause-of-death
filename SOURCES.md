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
- **How the source collects the data:** Administrative registration, not a survey.
  Numerators come from death certificates filed in the vital-records system of all
  50 states and DC; every certificate assigns exactly one *underlying* cause of
  death, coded to ICD-10 by NCHS. Denominators are Census Bureau population
  estimates matched to the mortality year. Universe is deaths of U.S. residents;
  it is effectively a complete count, not a sample.
- **How the source defines the data:**
  - *Underlying cause of death* = the single condition that initiated the chain of
    events leading to death (ICD-10 rules), not every condition present. A cause
    counted here can differ from "any mention" (multiple-cause) tabulations.
  - *ICD-10 113 Cause List*: causes prefixed with "#" are the non-overlapping,
    rankable leading-cause categories. Sub-causes and parent categories also appear
    and *do* overlap — summing across them double-counts.
  - *Race (Single Race 6)*: White, Black or African American, American Indian or
    Alaska Native, Asian, Native Hawaiian or Other Pacific Islander, More than one
    race. This is the post-1997-standard single-race coding, where multiple-race
    decedents are kept in a "more than one race" category rather than reassigned.
  - *Crude rate* = deaths ÷ population × 100,000 (this project modifies the
    denominator — see Methodology Notes).
- **Methodology changes / series breaks:**
  - **Single-race vs bridged-race break at 2018.** The "expanded" (single-race)
    UCD file only covers **2018 forward**. Earlier WONDER mortality uses
    *bridged-race* categories (multiple-race decedents reassigned to one race).
    Single-race death counts run **lower** than bridged-race counts for major race
    groups, so **race-specific counts are NOT comparable across the 2018 boundary**.
    This project uses 2018+ single-race data only, so no cross-break comparison is
    made — but do not splice these counts onto pre-2018 bridged-race series.
    (See NVSR Vol. 70 No. 3, "Comparability of Race-specific Mortality Data Based
    on 1977 Versus 1997 Reporting Standards.")
  - ICD-10 has been in use for U.S. mortality since 1999; there is no ICD revision
    break inside this project's window. (Cross-era work spanning the ICD-9→ICD-10
    change at 1999 would need NCHS comparability ratios — not relevant here.)
- **Known controversies / debates:** Whether abortion belongs in a "cause of death"
  comparison at all is a contested framing choice (abortions are not recorded on
  death certificates and are not in the WONDER universe); this project makes that
  comparison explicitly and documents the denominator choice in Methodology Notes.
  The WONDER counts themselves are standard and uncontroversial.
- **Notes:**
  - "Suppressed" values indicate counts of 1–9 (confidentiality protection).
  - Rates are flagged **unreliable** in the expanded dataset when the width of the
    95% confidence interval exceeds 160% of the rate. Treat suppressed/unreliable
    cells as low-precision, not as zero.
  - Population figures are Census Bureau estimates matched to the mortality year.
  - 2024 data may be provisional at retrieval; unlikely to affect leading-cause rankings.
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
- **How the source collects the data:** Model-based estimate, not a full census.
  The Monthly Abortion Provision Study (MAPS) combines monthly data collected from
  a *sample* of abortion providers with historical caseload data on every known
  provider, and runs a statistical model to estimate monthly abortions per state
  and nationally. The universe is clinician-provided abortions within the formal
  U.S. health care system.
- **How the source defines the data:** A *clinician-provided abortion* = an abortion
  provided through the formal health care system (in-clinic or via telehealth/shield-law
  provision by a clinician). This **excludes self-managed abortions** (e.g. pills
  obtained from non-U.S. pharmacies or community networks) and **excludes abortions
  provided within total-ban states**, so the figure is an **underestimate** of all
  abortions occurring. "Abortion rate" is per 1,000 women aged 15–44.
- **Methodology changes / series breaks:**
  - **Method break in 2023: APC → MAPS.** Guttmacher's long-running series was the
    **Abortion Provider Census (APC)** — a comprehensive census of all known providers
    conducted roughly every three years since 1974. The **Monthly Abortion Provision
    Study (MAPS)**, launched 2023, is a **different instrument**: a sample-plus-model
    estimate rather than a full census. MAPS monthly/annual figures are therefore
    **not a like-for-like continuation** of APC counts; Guttmacher itself compares
    2023–2024 MAPS estimates back to 2020 *APC* data with that caveat in mind. When
    citing "2020 vs 2024," note that 2020 is APC (census) and 2024 is MAPS (model).
  - Post-Dobbs (mid-2022) the provision landscape shifted structurally (bans, travel,
    telehealth, shield laws); year-over-year changes reflect real behavior change plus
    the method change above, so attribute movement carefully.
- **Known controversies / debates:** The exclusion of self-managed and total-ban-state
  abortions is a known, publisher-acknowledged undercount; estimates of self-managed
  volume vary and are debated. Guttmacher is a reproductive-rights research
  organization — its counts are widely used (including by researchers across the
  debate) but the framing of its releases is sometimes contested. Use the numbers,
  attribute the source, and note the undercount.
- **Notes:**
  - Full-year 2024 data released April 2025 (news release), with updated estimates
    in the June 2025 report revision.
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
- **How the source collects the data:** Aggregated administrative reporting. States
  and reporting areas *voluntarily* send CDC counts compiled from the abortion
  reports that providers file under each jurisdiction's own laws. There is no
  national reporting mandate, so participation and completeness vary by area and year.
- **How the source defines the data:** Definitions of what must be reported (and by
  whom) are set **per jurisdiction**, so the "reported abortion" is not defined
  identically everywhere. *Gestational age* reflects clinician measurement at time
  of abortion, tabulated only where known. This project uses the **age-group and
  gestational-age percentage distributions**, not CDC's absolute counts.
- **Methodology changes / series breaks:** The set of **reporting areas changes over
  time** — which states are included differs year to year, so CDC national totals
  are **not comparable across years as a level series**. Because this project uses
  only the *distributions* (which are far more stable than the counts) and applies
  them to a Guttmacher total, the reporting-area churn is a minor concern — but never
  compare CDC absolute counts across years without checking the reporting-area list.
- **Known controversies / debates:** CDC materially **undercounts** total abortions
  versus Guttmacher because major states (incl. CA) don't report; this gap is
  well documented and is exactly why Guttmacher is used for the total here. The
  distributions remain usable even though the counts are incomplete.
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
  - **Important:** The 2022 gestational age distribution is an **estimate** when
    applied to 2024 abortion totals. No 2024 gestational data exists yet. The
    assumption of stability is supported by historical surveillance showing
    <1pp/year change in gestational composition (2015–2022).
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
- **How the source collects the data:** Model-based estimate. Census postcensal
  population estimates start from the most recent decennial census and roll it
  forward with administrative data on births, deaths, and migration (the components
  of population change). Not a survey and not a fresh count.
- **How the source defines the data:** Resident population as of July 1 of the
  estimate year, by age/sex/race. Race uses the **single-race** categories that match
  the WONDER numerator (see source 1) so rates are internally consistent.
- **Methodology changes / series breaks:** **Single-race population estimates are
  only available 2018 forward**; bridged-race estimates ran through 2020 and were
  then discontinued. This is the denominator side of the same 2018 single-race break
  described in source 1 — so numerator and denominator break at the same boundary and
  stay consistent within this project's 2018+ window. Postcensal estimates are also
  revised after each decennial census (a "vintage" change); using one vintage
  end-to-end avoids mixing revisions.
- **Known controversies / debates:** Postcensal estimates accumulate error the
  further they are from the base census (undercount debates, migration estimation).
  Not material at the national aggregate level used here.
- **Notes:**
  - Population estimates come directly from WONDER output to ensure consistency
    between mortality rates and denominators.
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

### Series breaks & comparability (read before any cross-year comparison)

The point of this section is to stop apples-to-oranges comparisons. Two known
breaks touch this project's sources:

- **CDC WONDER single-race break at 2018.** The expanded single-race UCD file
  (numerator) and the single-race population estimates (denominator) both start in
  2018; earlier WONDER data uses *bridged-race* categories, and race-specific counts
  are **not comparable across 2018**. This project stays entirely within 2018+, so it
  never crosses the break — but do not splice these onto pre-2018 bridged-race series.
- **Guttmacher APC → MAPS method change at 2023.** Pre-2023 totals come from the
  **Abortion Provider Census** (a full census); 2023+ come from the **Monthly
  Abortion Provision Study** (a sample-plus-model estimate). A "2020 vs 2024" change
  mixes a census level with a modeled level — flag it wherever it appears in a chart
  or caption.

Everything charted in this project is single-year 2024, so no series is drawn
*across* either break; these notes exist to protect any future extension.

---

## Source Provenance in DuckDB

Every table in `data/project.duckdb` has a corresponding entry in the
`_sources` metadata table:

```sql
SELECT duckdb_table, source_name, methodology, series_breaks FROM _sources;
```

The `_sources` table carries provenance alongside the data itself. Columns:
`duckdb_table`, `source_name`, `url`, `license`, `notes`, `retrieved`, and — added
so methodology travels with the data — **`methodology`** (how the source collects and
defines the data) and **`series_breaks`** (dates/boundaries across which the numbers
are NOT comparable). Keep these in sync with the per-source sections above.

Two tables in the DB extend beyond the four sources documented above and carry their
own break notes in `_sources`:
- `mortality_trend_national` — CDC WONDER **1999–2020** (bridged-race era; **not**
  comparable to the 2018+ single-race expanded files — never splice the two).
- `shr_homicides_2024` — FBI Supplemental Homicide Reports (voluntary agency
  reporting; UCR→NIBRS transition affects year-over-year coverage).

---

## Discrepancies Between Sources

| Issue | Detail | Resolution |
|-------|--------|------------|
| Guttmacher vs CDC abortion totals | Guttmacher ~1.12M vs CDC ~613K (2022) | CDC excludes CA, MD, NH, NJ (~20% of abortions). Use Guttmacher. |
| Age proportions 2022 vs 2024 | Slight shift possible | Historical data shows <1pp/year change. Acceptable. |
| WONDER 2024 provisional vs final | 2024 data may be provisional | Noted; unlikely to affect rankings materially. |
