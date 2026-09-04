# Codebook — abortion_cause_of_death_v1

**Dataset:** Abortion compared to leading causes of death (United States, 2024)
**Rows:** 63 — leading causes under two scenarios (`Without abortion` /
`With abortion`), across three populations: `National`, `Female` (all ages), and
`Female 15-44`.
**Columns:** 14
**Author:** @unwelcomedata
**Sources:** CDC WONDER 2024 (mortality + population), Guttmacher Institute 2024
(abortion total), CDC Abortion Surveillance 2022 (age & gestational-age
distributions). Full attribution, collection methods, definitions, and series
breaks are in [SOURCES.md](../SOURCES.md).

This dataset ranks leading causes of death and then shows where the year's
abortion total would fall **if abortion were counted as a cause of death** — a
deliberate, contested framing that the project states openly. Abortions are not
recorded on death certificates and are not in the CDC WONDER universe; the
comparison is constructed, not drawn from a single source.

---

## Columns

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Calendar year of the mortality data (2024). |
| `category` | str | Population the ranking is computed over: `National` (all people), `Female` (all ages), or `Female 15-44` (the standard reproductive-age band). |
| `scenario` | str | `Without abortion` = leading causes as officially recorded. `With abortion` = the same list with the abortion total inserted and the ranking recomputed. |
| `rank` | int | Rank of the cause within its `category` × `scenario` (1 = most deaths). Null on the inserted abortion row before re-ranking. |
| `cause_code` | str | Source cause identifier: CDC ICD-10 113-cause-list code (e.g. `GR113-054`), or `ABORT` for the constructed abortion row. |
| `cause` | str | Plain-English cause name (e.g. Heart disease, Cancer, Accidents, Suicide, Homicide, Abortion). |
| `deaths` | int | Number of deaths (CDC WONDER underlying-cause count), or the abortion total (Guttmacher) on the abortion row. |
| `sex` | str | `Both`, `Female`, or `Male`. The abortion row is `Female`. |
| `population` | float | Resident population denominator for the group (CDC WONDER / Census, single-race), before any abortion adjustment. |
| `population_adjusted` | float | `population` + the year's abortion total. Used as the denominator in the "with abortion" rate so aborted lives are counted in the base, consistent with how crude death rates treat decedents. See SOURCES.md → Methodology Notes. |
| `crude_rate` | float | Deaths per 100,000 of `population`. Null where a rate is not meaningful (e.g. the raw abortion row). |
| `crude_rate_adjusted` | float | Deaths (or abortions) per 100,000 of `population_adjusted`. |
| `gestation_group` | str | For the abortion row only: gestational-age distribution of abortions (from CDC Abortion Surveillance 2022, applied to the 2024 total). Null for all other rows. |
| `data_source` | str | Short provenance string for the row (e.g. "CDC WONDER 2024 + Guttmacher 2024"). |

---

## Reading notes

- **The abortion figure is a Guttmacher MAPS *model* estimate**, not a census, and
  it *excludes* self-managed abortions and abortions in total-ban states — so it is
  an undercount of all abortions occurring. It is also a different instrument from
  Guttmacher's older Abortion Provider Census (a method break at 2023). See
  SOURCES.md.
- **Gestational-age and age distributions are 2022**, applied to the 2024 total on
  the assumption they change slowly (historically <1 percentage point per year).
- This export covers the **National / Female / Female 15-44** cuts. The
  race/ethnicity comparisons shown in some charts are derived in the project
  pipeline from the same CDC single-race data (2018 forward) but are not included
  as rows in this dataset file.
- Ranks are computed per `category` × `scenario`; do not compare a rank in one
  group to a rank in another without also comparing the underlying rates.
