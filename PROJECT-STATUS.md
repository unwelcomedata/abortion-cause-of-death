# abortion-cause-of-death — Project Status

**Last updated:** 2026-08-18
**Status:** IN PROGRESS — Social viz charts 1-3 complete, next session adds side-by-side comparisons.

---

## Current Phase: Social Visualization (04b-viz-social)

### Completed This Session

1. **Chart 1: National abortion comparison** — DONE
   - Title: "What if abortion was counted as a cause of death?"
   - Subtitle: "Top 5 causes of death among all Americans, by sex (2024)"
   - Stacked male (#005F73) / female (#E9D8A6) bars with % labels inside
   - Abortion bar (#AE2012) with gestation age dividers (#fff5e6 vertical lines)
   - Gestation labels: ≤9 wks (79%), 10-13 wks (14%) — smaller segments unlabeled
   - Direct "Male"/"Female" labels (top-aligned, inside Heart disease bar)
   - Total count to right of each bar (15px bold)
   - Footer: rule + source attribution + @unwelcomedata watermark

2. **Chart 2: White race comparison** — DONE
   - Same format as Chart 1, filtered to White Americans
   - Abortion count: 337,200 (30% of national, Guttmacher Patient Survey 2021-2022)
   - No gestation dividers (national proportions only)

3. **Chart 3: Black race comparison** — DONE
   - Same format, filtered to Black Americans
   - Abortion count: 325,960 (29% of national)
   - Subtitle: "Top 5 causes of death among Black Americans, by sex (2024)"

### New Shared Assets Created

- `shared/chart_templates.py` — Reusable chart functions:
  - `stacked_horizontal_bar()` — standard stacked bar with all features
  - `add_footer()` — standard footer (rule + source text) for any Altair chart
- `shared/viz.py` — Updated:
  - `SEX_COLORS`: Female=#ffe8cc, Male=#a8e0e0 (soft pastels)
  - `TEXT_COLORS`: on_dark=#E9D8A6, on_light=#003049
- `shared/bold_palettes.py` — Updated sex palette + text color constants
- `color_palettes/bold/PALETTE-VIEWER.html` — Updated with text colors section + new sex colors

### Data Added This Session

- `abortions` table now includes `race_pct` and `race_count` rows:
  - NH White: 30% → 337,200
  - Black: 29% → 325,960
  - Latinx: 30% → 337,200
  - Asian: 4% → 44,960
  - Other/multi-race: 7% → 78,680
  - Source: Guttmacher Abortion Patient Survey 2021-2022 applied to 2024 total

---

## Next Session Plan

### Charts to Build

4. **Male vs Female side-by-side** (top 10 causes each, national)
   - Two panels: left = male top 10, right = female top 10
   - Using stacked bar template but adapted for side-by-side layout
   - Same color scheme (#005F73 for male bars, #E9D8A6 for female bars)

5. **White race side-by-side** (male vs female top 10)
   - Same format as chart 4, filtered to White

6. **Black race side-by-side** (male vs female top 10)
   - Same format, filtered to Black

### Template Work

- Add `side_by_side_bars()` function to `shared/chart_templates.py`
- May need to adapt for `alt.hconcat()` or faceted layout

---

## Chart Style Reference (finalized)

| Element | Value |
|---------|-------|
| Male bar | #005F73 (Dark Teal) |
| Female bar | #E9D8A6 (Vanilla Custard) |
| Abortion bar | #AE2012 (Oxidized Iron) |
| Gestation dividers | #fff5e6 (Pale Warm) |
| Text on dark | #E9D8A6 |
| Text on light | #003049 |
| Total count text | #374151, 15px bold |
| Pct label text | 13px bold |
| Y-axis labels | 14px bold |
| Footer rule | #D1D5DB, 1px |
| Footer source text | #6B7280, 9px |
| Watermark | @unwelcomedata, bottom-right, Pillow |

---

## Environment

- Python: `/opt/anaconda3/envs/data_projects/bin/python` (3.13)
- DuckDB: `data/project.duckdb`
- GitHub: `unwelcomedata/abortion-cause-of-death` (private, main branch, clean)
