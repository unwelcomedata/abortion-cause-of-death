# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-20  
**Status:** IN PROGRESS — Pillow renderer built, refinements needed

---

## Current Phase: Viz Engine Migration (Altair → Pillow)

### What's Done
- Pillow-based chart renderer built in `shared/chart_templates.py` (side_by_side_bars, stacked_horizontal_bar, single_ranked_bars, detail_bar)
- `shared/chart_factory.py` rewritten — same `render_chart(config)` interface, routes to Pillow templates
- `src/viz_social.py` simplified to thin compatibility layer (no Altair/vl-convert)
- Inter font installed and loading correctly (Bold + Regular)
- Font metrics using `getmetrics()` for proper vertical centering
- All 5 charts render at 1600×900 without errors
- Stacked bar charts (2, 3, 4) look good
- Title rendered in Inter Bold, subtitle in Inter Regular, footer with source + watermark

### What Needs Fixing (Priority)

1. **Side-by-side bar alignment issues:**
   - Bars across left and right panels are vertically misaligned (bars at the same rank should sit on the same horizontal line)
   - Root cause: each panel computes `bars_y_start` independently after drawing its panel title. Need to synchronize the y-start across both panels.
   - Scale accuracy: both panels now share `bar_area_width` and `x_max`, but verify visually that a value like 28.5 in the right panel produces a longer bar than 26.8 in the left panel.

2. **Detail bar width:**
   - Currently computed from bar_area_left to bar_area_right — this is fragile and varies between charts
   - Consider: set a fixed detail bar width (e.g., 80% of total_chart_width) or anchor it to a simpler reference
   - The detail bar should feel like it belongs to the chart, not extend past where bars end

3. **Notebook cleanup (04b-viz-social.ipynb):**
   - Markdown header still says "Altair + vl-convert" — update to reflect Pillow
   - Remove any old Altair-specific cells/comments
   - Verify all cells run cleanly with the new pipeline

### What Needs Doing (Next Session)

1. Fix side-by-side vertical alignment (synchronize bars_y_start between panels)
2. Fix detail bar width (use a fixed proportion or anchor to right panel bar end)
3. Clean up `project-template/` for new viz rendering process
4. Go through all notebooks — remove outdated code/cells, update comments/headings
5. Make processes reproducible (confirm `04b-viz-social.ipynb` runs top-to-bottom)

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
