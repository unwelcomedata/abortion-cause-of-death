# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-21  
**Status:** NEAR COMPLETE — Charts finalized, posting plan done, notebooks 01-03 need reproducibility check

---

## Current Phase: Ready to Post (pending final reproducibility pass)

### What's Done
- Full Pillow-based chart pipeline operational (shared/chart_factory.py + shared/chart_templates.py)
- 6 charts rendered and finalized in `outputs/social/`:
  - `01_top10_causes_female_vs_male.png` — Chart 1
  - `02_top10_causes_white_vs_black.png` — Chart 2
  - `03_abortion_comparison_national.png` — Chart 3
  - `03b_top5_causes_white.png` — Chart 3b (supplemental)
  - `03c_top5_causes_black.png` — Chart 3c (supplemental)
  - `04_percapita_white_vs_black.png` — Chart 4
- Side-by-side bar alignment fixed (forced_bars_y_start)
- Detail bar width fixed (spans bar start to longest bar end)
- Two-line labels for narrow segments (inner segments + detail bars)
- Labels skip entirely when segment is too narrow to fit
- Consistent title/subtitle/source pattern across all charts
- Chart numbering matches posting strategy
- 04b-viz-social.ipynb runs top-to-bottom cleanly
- Notebooks cleaned: all Altair references removed
- social-posts.md complete (4-day posting plan, thread, methodology replies, rebuttals)
- project-template updated to Pillow pipeline (Altair/vl-convert removed)

### What Needs Doing (Next Session)

1. **Verify notebooks 01–03 run top-to-bottom** — confirm full pipeline reproducibility from raw data to export
2. **Final review of outputs** — spot-check exported CSV/Excel/Parquet in `export/`

### After This Project Is Wrapped

**Migrate dui-by-state to the same Pillow pipeline:**
- Replace Altair/vl-convert social charts with shared chart_factory approach
- Standardize title/subtitle/source pattern
- Verify 04b-viz-social.ipynb runs cleanly
- Update requirements.txt (remove Altair deps)
- Confirm all 4 publication charts render correctly

Once both projects are clean and reproducible, ready to take on the next idea.

---

## Architecture

```
Notebook cell: render_chart({config dict})
    ↓
shared/chart_factory.py: routes type → builder, loads DuckDB data
    ↓
shared/chart_templates.py: Pillow drawing (all chart types)
    ↓
PIL.Image → saved to outputs/social/*.png
```

No Altair, no vl-convert, no browser dependency. Pure Pillow.

### Key Files
- `shared/chart_factory.py` — entry point, data loading, routing, PNG export
- `shared/chart_templates.py` — all Pillow drawing logic (1100+ lines)
- `shared/viz.py` — brand palette, PRESETS, SOCIAL_THEME
- `src/viz_social.py` — thin save_social() wrapper
- `notebooks/04b-viz-social.ipynb` — chart configs + render calls

### DuckDB Tables (chart data)
chart_female_top10, chart_male_top10, chart_male_suicide_age,
chart_white_top10, chart_black_top10, chart_white_suicide_age,
chart_black_homicide_offender, chart_national_stacked, chart_stacked_white,
chart_stacked_black, chart_abortion_gestation, chart_annotations,
chart_white_percapita, chart_black_percapita

### Chart Title/Subtitle/Source Pattern
- **Title:** Statement or question. No year, no unit.
- **Subtitle:** Unit or scope ("Rate per 100,000 population")
- **Footer:** Source with year ("CDC WONDER 2024")

---

## Environment
- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13.5)
- Font: Inter Bold + Regular installed at `~/Library/Fonts/`
- DuckDB: `data/project.duckdb`
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch, clean)
