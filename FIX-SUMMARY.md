# Fix Summary: Scope Refinement & Chart Fix

## Issues Identified & Resolved

### 1. Charts Not Rendering (Root Cause)
The 03-prepare notebook had a fatal bug: **the `prepare_without()` function was defined but never called**. This resulted in:
- `without_national` was never created
- The export only contained ONE row per "With abortion" scenario (just the abortion row)
- Charts tried to find the top 5 causes in the "With abortion" data, but they didn't exist

### 2. Conceptual Scope Clarification (Statistical Rigor)
User raised critical points:
- **Female-only comparison was invalid:** Mixing female-stratified mortality with national-level abortion data (apples-to-oranges)
- **Female 15-44 made no sense:** Conflates "age of pregnant person" (15-44) with "age of fetal death" (no age)

**Decision:** Keep only the **National comparison**
- "If abortions were counted as a cause of death nationally, where would they rank?"
- Both abortion and mortality data are at the same national aggregation level
- No category mixing, no stratification mismatches
- All exploratory charts (by sex, by age) show mortality only, since we have abortion only as a national total

## What Fixed It

### 1. Rebuilt 03-prepare.ipynb
- Added proper function calls: `without_national = prepare_without(mort_national, 'National')`
- Added display_name mapping (Heart disease, Cancer, etc.)
- Ensured `build_with()` re-ranks abortion + top 10 causes together

### 2. Created scripts/generate_export.py
- Standalone Python script that properly generates export
- Exports only **National** comparison (21 rows: 10 without + 11 with)
- All 3 formats: CSV, Excel, Parquet

### 3. Updated 04-viz.ipynb
- **Chart 1:** National WITHOUT vs WITH abortion comparison (the main finding)
- **Chart 2:** Exploratory mortality by sex (no abortion)
- **Chart 3:** Exploratory mortality by age (no abortion)

### 4. Refactored PROJECT-PLAN.md
- Clearly documents why national-only comparison is the only valid one
- Explains why female-only and age-specific comparisons are invalid
- Removes all Female and Female 15-44 references

## Result

Export now contains exactly what makes sense:

**National, Without abortion**: 10 rows (Heart disease, Cancer, Accidents, ...)
**National, With abortion**: 11 rows (Abortion at rank 1, then top 10 ranked 2-11)

**Total: 21 rows, 1 category**

## How to Proceed

1. **In Jupyter:** Clear outputs and restart kernel
2. **Run 04-viz.ipynb** from top:
   - Chart 1: National comparison (main finding)
   - Charts 2-3: Exploratory mortality breakdowns (no abortion)
3. Continue with social chart prep (04b-viz-social.ipynb)

## Files Changed
- `/notebooks/03-prepare.ipynb` — Fixed, National-only export
- `/scripts/generate_export.py` — National-only export generation
- `/export/abortion_cause_of_death_v1.*` — Regenerated (21 rows)
- `/PROJECT-PLAN.md` — Completely refactored for scope clarity
- `/notebooks/04-viz.ipynb` — 3 charts, all statistically valid
