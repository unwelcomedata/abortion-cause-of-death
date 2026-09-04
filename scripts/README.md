# Scripts & reproducibility

This project is **not** a one-command rebuild. Two of the three sources are
**manual downloads** (CDC WONDER queries and the Guttmacher published total have
no bulk API), and the ingest → clean → prepare pipeline runs in the project
notebooks. This README documents the honest run order so a reader can trace
raw → charts → export.

## What requires manual work

1. **CDC WONDER** — run the queries listed in [`../SOURCES.md`](../SOURCES.md)
   (Underlying Cause of Death, Expanded) and export each as tab-delimited into
   `data/raw/` with the filenames given there
   (`wonder_mortality_2024.tsv`, etc.). WONDER is an interactive query tool; there
   is no scripted download.
2. **Guttmacher 2024 total** — transcribe the national abortion total and rate
   from the published Monthly Abortion Provision Study fact sheet (see SOURCES.md)
   into the raw CSV the ingest step expects.
3. **CDC Abortion Surveillance 2022** — the age and gestational-age distributions
   are transcribed from the published MMWR summary (SOURCES.md).

## Pipeline (after `data/raw/` is populated)

The ingest, cleaning, and preparation stages run in the numbered project
notebooks (they build the DuckDB tables `mortality_national`, `abortions`, and the
chart tables). The reusable logic lives in [`../src/`](../src) (`ingest.py`,
`clean_quality.py`, `prepare.py`, `viz.py`, `viz_social.py`).

Once the DuckDB tables are built, the published dataset is rebuilt with one script:

```bash
python scripts/generate_export.py    # DuckDB tables → export/ (CSV + codebook)
```

## Script descriptions

| Script | Reads | Writes | Notes |
|--------|-------|--------|-------|
| `generate_export.py` | DuckDB tables `mortality_national`, `abortions` | `export/abortion_cause_of_death_v1.*` | Builds the "with / without abortion" ranking table and writes CSV (+ Excel/Parquet). The codebook (`*_codebook.md`) is maintained alongside the export. |

## Honesty note

Because the sources are manual and the pipeline is notebook-driven, "reproduce"
here means: get the same raw files from the cited sources, run the documented
steps, and you will land on the same export. It is not a single scripted command,
and this README says so on purpose.
