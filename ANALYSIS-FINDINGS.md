# 04-viz.ipynb Analysis: Notable Patterns

## Overview
The exploratory visualization notebook (04-viz.ipynb) now includes systematic analysis of small multiples to identify noteworthy data patterns suitable for social media posts.

---

## Key Findings

### Sex-Based Patterns (Chart 4: Top 10 Causes by Sex × Age)

#### Extreme Male Dominance
- **Suicide: 79.8% Male** (4.0x more likely than female)
  - Sharp peak in males ages 15-64
  - Dramatic finding worth dedicated social chart

- **Accidents: 65.7% Male**
  - Strong across working-age and young adult years
  
- **Liver disease: 61.4% Male**
  - Consistent across age groups

#### Female Dominance
- **Alzheimer's: 67.9% Female** (2.1x more likely than male)
  - Increases dramatically in oldest age groups (80+)
  - Surprising finding: older women far more likely to die of Alzheimer's
  - **Validity check:** This is likely real due to:
    - Female life expectancy (women live longer → more exposure to Alzheimer's risk)
    - Female over-representation in oldest old cohorts (80+ years)
    - Possible sex differences in diagnosis/coding (less likely but possible)

- **Stroke: 56.1% Female**
  - Pronounced in oldest age groups

#### Moderate Patterns
- **Heart disease: 55.1% Male** - expected for leading cause
- **Diabetes: 57.2% Male** - expected endocrine pattern

---

### Race-Based Patterns (Chart 5: Top Causes by Race)

#### Race-Specific Causes in Top 7

**Kidney disease** (top 7 in):
- Black or African American
- Native Hawaiian or Other Pacific Islander
- Notable: higher prevalence of kidney disease in these communities
  
**Respiratory disease** (top 7 in):
- American Indian/Alaska Native
- Black or African American
- More than one race
- White
- **Nearly universal** (except Asian)

**Liver disease** (top 7 in):
- American Indian/Alaska Native only
- **Strong finding:** disparity marker for AI/AN populations

**Influenza/Pneumonia** (top 7 in):
- Asian only
- Unexpected finding: could reflect:
  - Age structure (more elderly in Asian subgroup)
  - Coding differences
  - Healthcare access patterns

**Suicide** (top 7 in):
- More than one race
- Native Hawaiian or Other Pacific Islander
- Notably absent from other racial groups' top 7
- **Important:** suggests specific mental health crises in these communities

**Alzheimer's** (top 7 in):
- Asian
- White
- Notably absent from Black, AI/AN, Native Hawaiian, Multi-race
- Could reflect:
  - Age structure differences
  - Diagnostic patterns
  - Competing causes of death

---

## Patterns Worth Individual Social Charts

### High Priority (Dramatic/Unexpected)

1. **Suicide sex disparity**
   - "Men are 4x more likely to die by suicide"
   - Visual: Side-by-side bars showing 79.8% vs 20.2%
   - Includes age pattern (concentrated in working/young-adult years)

2. **Alzheimer's sex disparity**
   - "Women are 2.1x more likely to die of Alzheimer's"
   - Visual: Shows divergence in oldest age groups
   - Include note: women live longer + female life expectancy advantage

3. **Liver disease in AI/AN**
   - "Liver disease in top 7 causes only for American Indian/Alaska Native"
   - Disparity marker showing unique health crisis in this community

4. **Kidney disease in Black/Native Hawaiian**
   - "Kidney disease in top 7 for Black and Native Hawaiian/PI populations"
   - Health equity story

### Medium Priority (Notable but Less Shocking)

- Accidents: 2x more male (65.7% vs 34.3%)
- Respiratory disease disparities (nearly universal except Asian)
- Stroke: slight female majority (56.1%)

### Lower Priority (Expected Patterns)

- Heart disease male majority (expected)
- Diabetes male majority (expected)

---

## Technical Notes

### Data Validation
- All percentages calculated from national mortality data (WONDER 2024)
- No age adjustment applied (raw counts, not rates)
- Small populations (e.g., Native Hawaiian/PI) have more volatility
- Sex categorization: Binary (Male/Female) only; consistent with WONDER coding

### Limitations
- Small multiples shown exploratory data; individual focused charts will be cleaner
- Age patterns compressed in small space; create dedicated age-specific charts for detail
- Race categories: OMB single race 6 (some data in "More than one race" category)
- No statistical significance testing (frequencies only)

---

## Recommended Next Steps

1. **Create focused individual charts** for top 3 findings (Suicide, Alzheimer's, Liver disease)
2. **Test social media messaging** around these findings
3. **Consider age-stratified versions** of Suicide (peaks in 15-64) and Alzheimer's (peaks in 80+)
4. **Validate race findings** with qualitative research on why these disparities exist
5. **Plan follow-up analysis** on what policy/health factors drive these patterns

---

## Files Generated

- `04_causes_sex_age_multiples_national.png` - Raw data (2×5 grid, all top 10 causes)
- `05_causes_age_multiples_race_*.png` - By race (6 files, 2×4 grids each)
- `03_causes_by_sex_national.png` - Stacked by sex (clean, labeled, publication-ready)
- `03b_national_without_vs_with_race_*.png` - Abortion comparison by race (2 files)
- `06_causes_by_sex_race_*_stacked.png` - By race + sex stacked (2 files: white, black)

See `notebooks/04-viz.ipynb` for full analysis code and visualization logic.
