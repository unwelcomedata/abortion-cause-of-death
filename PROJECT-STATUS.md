# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-19
**Status:** IN PROGRESS — Social viz complete (5 charts). Ready for posting plan.

---

## Current Phase: Social Visualization Complete

### Charts (04b-viz-social.ipynb)

1. **Chart 1: Female vs Male top 10 (per 100k)** — DONE
   - Side-by-side horizontal bars, shared x-scale
   - Female: #E9D8A6 (vanilla custard) | Male: #005F73 (dark teal)
   - Suicide highlighted #94D2BD on male panel, annotated "#16 for women"
   - Template: `side_by_side_bars()` in `shared/chart_templates.py`

2. **Chart 1b: White vs Black top 10 (per 100k)** — DONE
   - Same side-by-side template
   - White: #CA6702 (burnt caramel) | Black: #EE9B00 (gold orange)
   - Dual highlights (#BB3E03 accent):
     - Suicide on White panel: "#13 for Black"
     - Homicide on Black panel: "#19 for White"

3. **Chart 2: National Abortion Comparison** — DONE
   - Stacked male/female bars with abortion inserted
   - Gestation age dividers within abortion bar
   - Direct segment labels, % inside, total count right

4. **Charts 3 & 4: Abortion by Race (White & Black)** — DONE
   - Same stacked format as Chart 2, filtered by race
   - Race-specific abortion counts (Guttmacher 2024 proportions)

### Key Design Decisions

- **Per-capita rates** for all comparison charts (sex, race). Absolute counts only for abortion insertion charts (since abortion has no population denominator).
- **Shared x-scale** across panels for honest visual comparison.
- **Stable ranking** uses `ORDER BY rate DESC, deaths DESC` to break ties.
- **Color conventions**: Teal/vanilla for sex, gold/amber for race, red accent (#BB3E03) for both highlight bars.

---

## Shared Assets Updated This Session

- `shared/chart_templates.py` — Added `side_by_side_bars()`:
  - Supports `highlight` (right panel) and `highlight_left` (left panel)
  - Per-bar color via `_bar_color` column with `scale=None`
  - Annotation text (italic, #6B7280, positioned dx=62 from bar end)
  - Configurable panel width, height, spacing, font sizes

---

## Files Removed (iteration artifacts)

- `FIX-SUMMARY.md` — debugging notes (no longer relevant)
- `PALETTE-IMPLEMENTATION.md` — palette decisions captured in `shared/viz.py`
- `SESSION-SUMMARY.txt` — old session handoff
- `SOCIAL-VIZ-READY.md` — outdated chart list
- Stale PNGs in `outputs/social/` (18 files removed)

---

## What Remains

- `PROJECT-PLAN.md` — data methodology and scope decisions (keep)
- `ANALYSIS-FINDINGS.md` — statistical findings from the data (keep)
- `SOURCES.md` — full attribution (keep)
- `README.md` — project overview (keep)

---

## Next Steps (if reopening)

- [ ] Write social posting plan (copy, alt text, thread strategy)
- [ ] Consider additional charts:
  - Alzheimer's disparity by race (2x higher for White — age structure effect)
  - Diabetes/kidney cluster (30% higher rate for Black)
  - Accidents by sex × race small multiples
- [ ] Age-adjusted rates version (for methodological rigor in academic contexts)

---

## Environment

- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13)
- DuckDB: `data/project.duckdb`
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch)
