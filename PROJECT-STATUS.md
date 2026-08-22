# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-22  
**Status:** COMPLETE — Pipeline rebuilt with corrected NH race/ethnicity data. 12 charts. Ready to post.

---

## Current Phase: Ready to Post

### What's Done
- Full Pillow-based chart pipeline operational (shared/chart_factory.py + shared/chart_templates.py)
- Pipeline rebuilt with correct Non-Hispanic race categories (aligned with Guttmacher)
- `cause_display_names` table in DuckDB — single source of truth for chart labels (no hardcoding)
- 12 charts rendered in `outputs/social/`:
  - `01_top10_causes_female_vs_male.png` — Chart 1
  - `02_top10_causes_white_vs_black.png` — Chart 2
  - `02b_top10_causes_white_vs_hispanic.png` — Chart 2b
  - `02c_top10_causes_black_vs_hispanic.png` — Chart 2c
  - `02d_top10_causes_3way.png` — Chart 2d (experimental 3-way)
  - `03_abortion_comparison_national.png` — Chart 3
  - `03b_top5_causes_white.png` — Chart 3b
  - `03c_top5_causes_black.png` — Chart 3c
  - `03d_top5_causes_hispanic.png` — Chart 3d
  - `04_percapita_white_vs_black.png` — Chart 4
  - `04b_percapita_white_vs_hispanic.png` — Chart 4b
  - `04c_percapita_black_vs_hispanic.png` — Chart 4c
- Full pipeline reproducibility verified (01-ingest → 02-clean → 03-prepare → 04b-viz-social)
- social-posts.md updated with corrected rates and source credibility section
- Gestation footnote added to chart 3 source line

### Posting Plan (unchanged from before)
- Charts 1-4 for initial 4-day posting sequence (no Hispanic — save for follow-up)
- Hispanic charts (2b, 2c, 3d, 4b, 4c) available as supplemental/reply content
- 2d (3-way) is experimental — may be too cramped for mobile

### Key Data (corrected NH rates)
- NH White abortion rate: 172.2/100k (#3)
- NH Black abortion rate: 753.2/100k (#1)
- Hispanic abortion rate: 492.8/100k (#1)
- Black/Hispanic ratio: 1.53×
- Hispanic/White ratio: 2.86×
- Black/White ratio: 4.37×

### Bug Fixed This Session
- Population bug in chart_female/male_top10: was using MAX(population) of single age group (~12M) instead of SUM of all age groups (~168M). Rates were 14× inflated.

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

### Key Files
- `shared/chart_factory.py` — entry point, data loading, routing, PNG export
- `shared/chart_templates.py` — all Pillow drawing logic
- `shared/viz.py` — brand palette, PRESETS, SOCIAL_THEME
- `notebooks/04b-viz-social.ipynb` — chart configs + render calls

### DuckDB Tables (key)
- `cause_display_names` — CDC name → chart display name mapping (30 entries)
- `mortality_race_ethnicity` — WONDER Sex × Hispanic Origin × Race × Cause (2024)
- `mortality_nh_white`, `mortality_nh_black`, `mortality_hispanic` — aggregated
- `chart_*_top10`, `chart_*_percapita`, `chart_stacked_*` — ready for rendering

---

## Environment
- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13.5)
- Font: Inter Bold + Regular installed at `~/Library/Fonts/`
- DuckDB: `data/project.duckdb` (35 tables)
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch, clean)
