# Project Plan: abortion-cause-of-death

## Central Question

**"What if abortions were treated as a cause of death?"**

Abortion is not classified as a death in vital statistics. This project takes
reported abortion counts and inserts them into the leading-causes-of-death
ranking — nationally — to visualize where abortion would land if it were
counted the same way as heart disease, cancer, etc.

---

## Data Sources

### 1. CDC WONDER — Mortality by Race × Sex (2024)

- **File:** `data/raw/wonder_mortality_2024.tsv`
- **Dimensions:** Single Race 6 × Sex × ICD-10 113 Cause List
- **Year:** 2024
- **Rows:** ~1,688 (after filtering notes)
- **Use:** Aggregate across race and sex to get national totals.

### 2. CDC WONDER — Mortality by Sex × Age (2024)

- **File:** `data/raw/wonder_mortality_gender_2024.tsv`
- **Dimensions:** Sex × Five-Year Age Groups × ICD-10 113 Cause List
- **Year:** 2024
- **Rows:** ~5,092
- **Use:** Exploratory analysis (by sex, by age) — mortality only, no abortion comparison.

### 3. CDC WONDER — Mortality by Race × Age (2024)

- **File:** `data/raw/wonder_mortality_ages_2024.tsv`
- **Dimensions:** Single Race 6 × Five-Year Age Groups × ICD-10 113 Cause List
- **Year:** 2024
- **Rows:** ~17,116
- **Use:** Exploratory analysis (by age) — mortality only.

### 4. CDC WONDER — Mortality by Sex × Race (2018–2024 aggregate)

- **File:** `data/raw/wonder_mortality_gender_2018_2024.tsv`
- **Dimensions:** Sex × Single Race 6 × ICD-10 113 Cause List (aggregated over 7 years)
- **Year:** 2018–2024 (combined)
- **Rows:** ~1,793
- **Use:** Supporting reference for multi-year trends.

### 5. Guttmacher Institute — U.S. Abortion Estimates (PRIMARY for abortion counts)

- **What:** Total U.S. abortions and demographic breakdowns (age, gestational age)
- **Where:** https://www.guttmacher.org/article/2024/03/new-data-indicate-abortions-increased-2023
- **Year:** 2024 (Guttmacher Monthly Abortion Provision Study, released April 2025)
- **Key figures (2024):** 1,124,000 abortions nationally
- **Age proportions:** From CDC Abortion Surveillance 2022 (most recent with age detail)
- **Format:** Report text + tables (manually extracted to CSV)
- **Ingestion approach:** Manually enter verified figures into `data/raw/guttmacher_abortions.csv`

### 6. CDC Abortion Surveillance (cross-reference)

- **What:** CDC's annual Abortion Surveillance report (MMWR)
- **Limitation:** Excludes CA, MD, NH, DC in some years; 2–3 years behind
- **Use:** Validate Guttmacher totals and age distribution. Not primary source.

---

## Analytical Framework

### The Core Comparison

**Question:** If abortions were counted as a cause of death nationally, where would they rank among all causes of death for the entire population?

**Why national only?** Any stratification (female-only, age-specific, race-specific) creates category mismatches:
- We have abortion as a **national aggregate** (no age, no race breakdown)
- Comparing it to **stratified mortality** (female deaths, age-specific deaths) is invalid
- Female deaths ≠ female-only comparison; abortion is a national event
- Age-specific comparison conflates "age of pregnant person" with "age of fetal death"

### Valid Comparisons

| Comparison | Rationale | Shown |
|---|---|---|
| National overall: top causes vs abortion | National aggregation level matches abortion data | ✓ Main chart |

### Invalid Comparisons (Not Included)

| Comparison | Why invalid |
|---|---|
| Female-only vs abortion | Abortion is national; mixing stratified mortality with unstratified abortion |
| Age-specific vs abortion | Abortion has no age; conflates mother's age with fetal death |
| Race-specific vs abortion | Abortion not stratified by race in this analysis |

---

## Pipeline Stages

### Stage 1: Ingest (`src/ingest.py` + `01-ingest.ipynb`)

| Task | Source | Output |
|------|--------|--------|
| Load WONDER race × sex (2024) | `data/raw/wonder_mortality_2024.tsv` | DuckDB `mortality_race_sex` |
| Load WONDER race × age (2024) | `data/raw/wonder_mortality_ages_2024.tsv` | DuckDB `mortality_race_age` |
| Load WONDER sex × age (2024) | `data/raw/wonder_mortality_gender_2024.tsv` | DuckDB `mortality_sex_age` |
| Load WONDER sex × race (2018–24) | `data/raw/wonder_mortality_gender_2018_2024.tsv` | DuckDB `mortality_sex_race_trend` |
| Load Guttmacher abortion data | `data/raw/guttmacher_abortions.csv` | DuckDB `abortions` |

All WONDER files are already downloaded (manual query). Guttmacher data is manually compiled from published report.

### Stage 2: Clean (`src/clean_quality.py` + `02-clean.ipynb`)

All cleaning in DuckDB:

1. **Parse WONDER format** — strip notes/footer rows, cast Deaths and Population to integer
2. **Filter causes** — keep only ICD-10 113 "leading cause" groups (codes starting with #)
3. **Standardize names** — clean up cause names (remove ICD codes), normalize age group labels
4. **Create aggregated views:**
   - `mortality_national` — all causes summed across race and sex
   - `mortality_by_sex_age` — both sexes by age band and cause (for exploratory analysis only)
5. **Quality checks** — row counts, totals match published NVSS figures

**DuckDB tables after cleaning:**
- `mortality_race_sex` — raw parsed (2024)
- `mortality_race_age` — raw parsed (2024)
- `mortality_sex_age` — raw parsed (2024)
- `mortality_sex_race_trend` — raw parsed (2018–24)
- `mortality_national` — aggregated national totals by cause
- `mortality_by_sex_age` — both sexes by age band and cause
- `abortions` — Guttmacher data (national, by age)
- `_sources` — provenance metadata

### Stage 3: Prepare / Export (`src/prepare.py` + `03-prepare.ipynb`)

**Goal:** Organize mortality + abortion data into publication-ready tables with readable cause names.

1. **Cause name standardization:**
   - Apply human-readable shortcuts (e.g., "Heart disease" vs "Diseases of heart")
   - Use common/colloquial names (e.g., "Suicide" vs "Intentional self-harm")

2. **Population calculations:**
   - `population` = living population from WONDER
   - `population_adjusted` = `population + 1,124,000` (abortions added to denominator)
   - Rationale: Aborted lives never counted in population; adding them ensures consistent rate calculations

3. **Build "Without abortion" table (National only):**
   - Top 10 causes nationally by deaths, both sexes aggregated
   - Columns: `rank, cause, deaths, population, population_adjusted, crude_rate, crude_rate_adjusted`

4. **Build "With abortion" table (National only):**
   - Insert abortion (1,124,000) as a single row
   - Add gestational breakdown (≤9w, 10–13w, 14–20w, ≥21w)
   - Re-rank all causes including abortion
   - Recalculate crude rates using `population_adjusted`
   - Result: 11 rows (10 causes + abortion)

5. **Master export table:**
   - Combine WITHOUT and WITH scenarios
   - Columns: `year, scenario (Without/With), rank, cause, deaths, population, population_adjusted, crude_rate, crude_rate_adjusted, gestation_group (abortion only), data_source`
   - 21 rows total (10 without + 11 with)

6. **Export to files:**
   - `export/abortion_cause_of_death_v1.csv` (master table)
   - `export/abortion_cause_of_death_v1.xlsx` (National sheet)
   - `export/abortion_cause_of_death_v1.parquet` (columnar)
   - `export/abortion_cause_of_death_v1_codebook.md` (column definitions)

### Stage 4: Visualize (`src/viz.py` + `04-viz.ipynb` + `04b-viz-social.ipynb`)

#### Exploration charts (matplotlib, `04-viz.ipynb`):

**Chart 1: National — Without vs With Abortion**
- Left: Top 5 causes (all persons, both sexes)
- Right: Same 5 causes + abortion as additional bar
- Shows where abortion ranks among leading causes nationally

**Chart 2: Top Causes by Sex (Mortality Only)**
- Exploratory: Compare male vs female leading causes
- No abortion comparison (unstratified abortion vs stratified mortality)

**Chart 3: Female Age Subgroups (Mortality Only)**
- Exploratory: Top causes by age band (15–19, 20–24, ..., 40–44)
- No abortion comparison (abortion not stratified by age)

#### Social charts (Altair, `04b-viz-social.ipynb`):

**Chart 1: National — Without vs With (publication-ready)**
- Left: "Leading Causes of Death, USA 2024" — top 5, stacked by sex (Female | Male)
- Right: "If Abortion Were a Cause of Death" — top 5 + abortion, stacked by sex; abortion bar broken down by gestational week (≤9w | 10–13w | 14–20w | ≥21w)
- Format: `twitter_landscape`
- Watermark: `@unwelcomedata`
- Source: CDC WONDER 2024 + Guttmacher Institute 2024

**All charts:**
- Style: minimal, no chartjunk, bold left-aligned title, small subtitle with year/source
- Color palette: consistent across all charts; gestational age uses distinct colors

---

## Decisions (Resolved)

1. **National only.** The comparison requires matching aggregation levels. Only national abortion vs national mortality is valid.

2. **Rate methodology: Add abortions to population denominator.** Aborted lives were never counted in the population; adding them ensures consistent crude rate calculations.

3. **No race stratification.** Race data is retained in DuckDB for reference but not featured in primary analysis.

4. **Top 10 causes.** Primary export includes top 10 causes; main chart highlights top 5.

5. **Horizontal bar charts.** The story is about scale and rank. Bars are clearest for magnitude comparison.

---

## Validation Protocol

### Required checks:

1. **Mortality totals**
   - WONDER total deaths (all causes, both sexes) should be ~3.3M for 2024
   - Heart disease should be ~680–700K nationally
   - Spot-check against published NVSS preliminary report

2. **Guttmacher total validation**
   - Confirm published figure (1.124M for 2024)
   - Cross-reference against CDC Abortion Surveillance for overlapping years

3. **The headline claims**
   - Verify: Guttmacher total > heart disease deaths (1.124M > 683K ✓)
   - Show the math explicitly in the notebook

4. **Rate calculation audit**
   - crude_rate = deaths / (pop + abortions) × 100K
   - Compare calculated rates against WONDER's own published rates (should match closely)

---

## Raw Data Files on Hand

| File | Dimensions | Year | Rows |
|------|-----------|------|------|
| `wonder_mortality_2024.tsv` | Race × Sex × Cause | 2024 | 1,688 |
| `wonder_mortality_ages_2024.tsv` | Race × Age × Cause | 2024 | 17,116 |
| `wonder_mortality_gender_2024.tsv` | Sex × Age × Cause | 2024 | 5,092 |
| `wonder_mortality_gender_2018_2024.tsv` | Sex × Race × Cause | 2018–2024 | 1,793 |

All: tab-separated, ICD-10 113 Cause List (137 cause categories), with notes/footer section at bottom.

---

## File Checklist

Before marking COMPLETE:

- [ ] `config.yaml` — sources populated with metadata
- [ ] `SOURCES.md` — full attribution for all data sources
- [ ] `data/raw/` — all source files present, unmodified
- [ ] `data/project.duckdb` — all tables loaded, `_sources` populated
- [ ] `export/` — CSV + Excel + Parquet + codebook
- [ ] `outputs/` — exploratory PNGs saved
- [ ] `outputs/social/` — publication-ready PNGs (watermarked)
- [ ] `README.md` — project description + AI-assisted disclosure
- [ ] Charts validated against source data
- [ ] No notebook outputs committed
- [ ] Repo pushed clean to GitHub
