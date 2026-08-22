# abortion-cause-of-death

> **AI-Assisted Development**
> This project was built with the assistance of [Kiro](https://kiro.dev),
> an AI-powered development environment. All data sourcing decisions,
> methodology choices, and published findings are the responsibility of the
> author. AI was used for code generation, data pipeline construction, and
> research assistance — not for analysis conclusions or editorial judgment.

---

## What This Is

A mortality comparison showing how abortion would rank against leading
causes of death in the United States, using CDC WONDER 2024 mortality data
and Guttmacher Institute 2024 abortion estimates.

**Key outputs:**
- 6 publication-ready social charts (side-by-side bars, stacked bars, per-capita comparison)
- Exportable dataset (CSV, Excel, Parquet) with 63 rows across 3 comparison categories
- Full DuckDB analytical database with 32 tables

**Key findings:**
- At 1.12 million per year, abortion would rank between #1 (heart disease) and #2 (cancer) nationally
- For Black Americans, abortion would rank #1 at 695 per 100k — above heart disease
- For White Americans, abortion would rank #3 at 132 per 100k
- 93% of abortions occur by 13 weeks gestation (CDC Surveillance 2022 estimate)

---

## Data Sources

All data sources are documented in [SOURCES.md](SOURCES.md) with full
attribution, URLs, licenses, and retrieval notes.

Source provenance is also recorded inside the project database:

```sql
-- Open data/project.duckdb and run:
SELECT * FROM _sources;
```

---

## Project Structure

```
abortion-cause-of-death/
├── config.yaml              ← sources, paths, export settings
├── SOURCES.md               ← full data source attribution
├── ANALYSIS-FINDINGS.md     ← statistical findings and methodology
├── requirements.txt
├── data/
│   ├── raw/                 ← original downloaded files, never modified
│   ├── interim/             ← cleaned Parquet files
│   └── project.duckdb       ← single-file database (32 tables)
├── export/                  ← packaged datasets (CSV, Excel, Parquet)
├── outputs/
│   └── social/              ← 6 publication-ready chart PNGs
├── shared/                  ← (workspace-level) chart_factory + chart_templates
├── notebooks/
│   ├── 01-ingest.ipynb      ← fetch sources → data/raw/ → DuckDB
│   ├── 02-clean.ipynb       ← clean + quality checks → data/interim/
│   ├── 03-prepare.ipynb     ← export packaging (with/without abortion comparison)
│   ├── 04-viz.ipynb         ← exploratory charts (matplotlib)
│   ├── 04b-viz-social.ipynb ← publication social charts (Pillow pipeline)
│   └── 05-analysis.ipynb    ← statistical analysis
└── src/
    ├── ingest.py            ← fetch helpers (caching, rate limiting)
    ├── clean_quality.py     ← DuckDB cleaning + quality reports + _sources
    ├── prepare.py           ← PII stripping, codebook, packaging
    ├── viz.py               ← matplotlib chart builders (exploratory)
    └── viz_social.py        ← thin wrapper for shared Pillow pipeline
```

---

## Chart Pipeline

All publication charts are rendered via the shared workspace-level Pillow pipeline:

```
shared/chart_factory.py  → routes config dict to appropriate builder
shared/chart_templates.py → pure Pillow drawing (no browser dependency)
```

Charts render deterministically from DuckDB-stored
data tables prefixed with `chart_`.

**Publication charts (6):**
1. Top 10 causes: Female vs Male (side-by-side bars)
2. Top 10 causes: White vs Black (side-by-side bars + detail bars)
3. National abortion comparison (stacked bars + gestation inner segments)
3b. White Americans (stacked bars) — supplemental
3c. Black Americans (stacked bars) — supplemental
4. Per-capita: White vs Black (side-by-side bars, shared scale)

---

## Reproducibility

The full pipeline runs top-to-bottom:

```bash
# From project root, using the data_projects conda environment:
jupyter nbconvert --execute notebooks/01-ingest.ipynb
jupyter nbconvert --execute notebooks/02-clean.ipynb
jupyter nbconvert --execute notebooks/03-prepare.ipynb
jupyter nbconvert --execute notebooks/04b-viz-social.ipynb
```

All intermediate data is regenerated from raw files. Export files and charts
are deterministic given the same raw inputs.

---

## Export

```
export/
├── abortion_cause_of_death_v1.csv       (63 rows × 14 columns)
├── abortion_cause_of_death_v1.parquet
└── abortion_cause_of_death_v1.xlsx      (3 sheets: National, Female, Female_15-44)
```

Each row is a cause of death with columns for category (National/Female/Female 15-44),
scenario (with/without abortion), deaths, population, crude rate, and gestation group.

---

## Methodology Notes

- **Mortality data:** CDC WONDER 2024, ICD-10 113 Cause List, crude rates
- **Abortion counts:** Guttmacher Institute 2024 (1,124,000 clinician-provided)
- **Gestational age distribution:** CDC Abortion Surveillance 2022 (most recent
  year with gestation detail; applied to 2024 total as an estimate)
- **Rate formula:** `crude_rate = count / (population + abortions) × 100,000`
- **Race proportions:** Guttmacher Abortion Patient Survey 2021-2022
- Crude rates used (not age-adjusted) because age-specific abortion counts by
  race don't exist at the necessary granularity

See [SOURCES.md](SOURCES.md) for full source documentation and
[ANALYSIS-FINDINGS.md](ANALYSIS-FINDINGS.md) for statistical details.

---

## Anonymity

Commits are authored as `unwelcomedata`. Data files, exports, outputs, and
`.env` secrets are excluded from version control via `.gitignore`.
