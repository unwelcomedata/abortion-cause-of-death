# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-21  
**Status:** IN PROGRESS — Pillow renderer working, charts aligned, notebooks clean

---

## Current Phase: Viz Engine Complete — Ready for Final Polish

### What's Done
- Pillow-based chart renderer built in `shared/chart_templates.py` (side_by_side_bars, stacked_horizontal_bar, single_ranked_bars, detail_bar)
- `shared/chart_factory.py` rewritten — same `render_chart(config)` interface, routes to Pillow templates
- `src/viz_social.py` simplified to thin compatibility layer (no Altair/vl-convert)
- Inter font installed and loading correctly (Bold + Regular)
- Font metrics using `getmetrics()` for proper vertical centering
- All 5 charts render at 1600×900 without errors
- **Side-by-side bar alignment FIXED** — bars_y_start synchronized across panels via forced_bars_y_start
- **Detail bar width FIXED** — uses full content width (margin-to-margin) for stable sizing
- Stacked bar charts (2, 3, 4) look good
- Notebooks cleaned: Altair references removed, 04b header updated, outputs cleared
- 04b-viz-social.ipynb confirmed to run top-to-bottom cleanly

### What Needs Fixing (Lower Priority)

1. **Narrow segment label clipping:**
   - In the gestational age detail bar, the rightmost segment ("≥21 wks (1%)") clips at the image edge
   - Fix: skip label if segment width < label width, or shift label left

2. **Leftover files in outputs/social/:**
   - `01_top10_causes_female_vs_male_detail.png` (old composite approach)
   - `template_top10_by_sex.png` (dev template)
   - Can be deleted when ready to ship

### What Needs Doing (Next Session)

1. Clean up `project-template/` for new Pillow viz process (remove Altair workflow references)
2. Go through notebooks 01–03 — verify top-to-bottom reproducibility
3. Final chart review: decide if narrow segment label issue is worth fixing before posting
4. Write social-posts.md (posting plan, copy, alt text)

---

## Architecture (Current)

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
- `shared/chart_templates.py` — all Pillow drawing logic
- `shared/viz.py` — brand palette, PRESETS, SOCIAL_THEME (unchanged)
- `src/viz_social.py` — thin save_social() wrapper (barely needed now)
- `notebooks/04b-viz-social.ipynb` — the notebook (config cells unchanged)

### DuckDB Tables (chart data)
chart_female_top10, chart_male_top10, chart_male_suicide_age,
chart_white_top10, chart_black_top10, chart_white_suicide_age,
chart_black_homicide_offender, chart_national_stacked, chart_stacked_white,
chart_stacked_black, chart_abortion_gestation, chart_annotations

---

## Environment
- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13.5)
- Font: Inter Bold + Regular installed at `~/Library/Fonts/`
- DuckDB: `data/project.duckdb`
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch)
