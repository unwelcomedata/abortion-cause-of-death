# Project Status: abortion-cause-of-death

**Last Updated:** August 17, 2026  
**Current Phase:** Exploratory Viz Complete → Ready for Social Media Publishing + Deep Dives  
**Repo:** `unwelcomedata/abortion-cause-of-death` (private)

---

## ✓ COMPLETE & READY FOR SOCIAL VIZ

### Production-Ready Charts (Commit `1ee86fa`)

1. **Chart 1: National Abortion Comparison**
   - File: `outputs/01_national_without_vs_with.png`
   - Format: Side-by-side (without abortion | with abortion)
   - Status: **DEFINITE** for social media
   - Message: "If abortion were the leading cause of death in the US..."

2. **Chart 3: Top 10 Causes by Sex (Stacked)**
   - File: `outputs/03_causes_by_sex_national.png`
   - Format: Horizontal stacked bars, percent labels within bar, total count on right
   - Status: **DEFINITE** for social media
   - Message: Focus on dramatic sex differences (suicide 79.8% male, Alzheimer's 67.9% female)

3. **Chart 3b: Abortion Comparison by Race (2 figures)**
   - Files: `outputs/03b_national_without_vs_with_race_white.png`
   - Files: `outputs/03b_national_without_vs_with_race_black_or_african_american.png`
   - Format: Matches Chart 1 (side-by-side comparison)
   - Status: **DEFINITE** for social media
   - Messages: Race-specific abortion impact comparison

### Key Findings Identified

| Finding | Data Point | Chart |
|---------|-----------|-------|
| Suicide Dominance in Males | 79.8% male (4.0x vs female) | Chart 3 |
| Alzheimer's Dominance in Females | 67.9% female (2.1x vs male) | Chart 3 |
| Accidents Male-Heavy | 65.7% male | Chart 3 |
| Liver Disease Male-Heavy | 61.4% male | Chart 3 |
| National Abortion Impact | Would be #2-3 leading cause | Chart 1 |
| Race-Specific Abortion Impact | Different ranking by race | Chart 3b |

---

## 🔍 EXPLORATION BACKLOG (Next Session)

### High Priority: Detailed Analysis Needed

#### 1. **Accidents Breakdown**
- **Question:** What types of accidents? Motor vehicle? Falls? Suffocation? Poisoning?
- **Why:** Sensationalized finding—accidents are surprisingly #3-4 overall cause
- **Data Needed:**
  - ICD-10 code breakdown (V01-Y89 range for "accidents")
  - Check if CDC WONDER provides sub-category detail for "Accidents (unintentional injuries)"
  - May need to access raw WONDER query interface or different data cube
- **Hypothesis:** Traffic dominates; falls in elderly? Poisoning (opioids) in younger cohorts?
- **Social Angle:** Different messaging for "young people dying in car crashes" vs "elderly dying from falls"

#### 2. **Homicide by Perpetrator Race**
- **Question:** For homicides (top 10 for Black/African American), what % killed by which races?
- **Why:** Politically charged; need accurate data to counter stereotypes or correct assumptions
- **Data Needed:**
  - CDC WONDER likely doesn't have "perpetrator race" (victim-centric)
  - May need FBI UCR (Uniform Crime Reporting) or CDC's violence data products
  - Check: CDC National Violent Death Reporting System (NVDRS) — includes perpetrator info
  - Alternative: NIJ (National Institute of Justice) homicide data
- **Expected Pattern:** Likely majority same-race; smaller % inter-racial
- **Social Angle:** "Most homicides are intra-racial, not inter-racial"

#### 3. **Homicide by Age Breakdown**
- **Question:** At what age is homicide the leading/top-10 cause?
- **Why:** Expect peak in teens/20s; validate if true across races
- **Data Available:** mort_by_sex_age table (sex × age × cause)
- **Query:** Filter to homicide, pivot by age group, show trend
- **Social Angle:** "Homicide is leading cause of death for Black men ages 15-34" (if true)

#### 4. **Cause-Specific Demographics: "Unique to Group" Analysis**
- **Question:** For each cause, which demographic group(s) claim it in top 10?
- **Why:** Identify health disparities and group-specific crises
- **Data Structure:**
  - By sex: Which causes in men's top 10 but not women's (and vice versa)?
  - By race: Which causes in some races' top 10 but not others?
  - By age: Which causes age-specific (teen suicides vs. Alzheimer's in 85+)?
  - By sex + race: Which causes unique to specific intersections?
- **Examples Already Found:**
  - Suicide: top 10 for males, not females; top 7 for Multi-race & Native Hawaiian/PI only
  - Alzheimer's: top 7 for Asian & White only (not Black, AI/AN, Native Hawaiian, Multi-race)
  - Liver disease: top 7 for AI/AN only
  - Kidney disease: top 7 for Black & Native Hawaiian/PI only
- **Social Angle:** "Homicide is the leading cause of death for young Black men—but not for White men"

---

## 📊 DATA SOURCES & AVAILABILITY

### Currently Loaded (in `project.duckdb`)
- ✓ WONDER 2024: Mortality by sex × age × cause
- ✓ WONDER 2024: Mortality by race × sex × cause
- ✓ WONDER 2024: Mortality by race × age × cause
- ✓ Guttmacher: National abortion count + age breakdown

### NOT YET LOADED (Needed for Explorations)
- ✗ Accident sub-types (ICD-10 V01-Y89 detail) — may need new WONDER query
- ✗ Perpetrator race for homicides — likely need NVDRS or UCR data
- ✗ Detailed age breakdowns (5-year groups vs. single years) — may have more granularity

---

## 🎯 NEXT SESSION TASKS

### Phase 1: Validate Existing Findings (30 min)
- [ ] Run Chart 4 & Chart 5 exploratory analysis again
- [ ] Double-check sex/race patterns identified
- [ ] Document top 3 findings for social media campaign

### Phase 2: Accidents Deep Dive (45 min)
- [ ] Query CDC WONDER for accident ICD-10 breakdown (if available)
- [ ] If not in WONDER, document limitation
- [ ] Create hypothesis-driven chart: Motor vehicle vs. other accidents by age/sex

### Phase 3: Homicide Research (45 min)
- [ ] Research NVDRS/UCR data availability and access
- [ ] Assess effort to integrate perpetrator race data
- [ ] Create homicide by age chart (if data allows)

### Phase 4: Build "Unique Cause" Analysis (60 min)
- [ ] Systematically iterate through all 52 causes
- [ ] Identify which demographic groups claim each in top 10
- [ ] Create summary table: Cause × (Sex, Race, Age Group) showing unique claim
- [ ] Visualize top 5-10 most "disparate" causes (biggest demographic concentration)

### Phase 5: Prepare for 04b-viz-social.ipynb (60 min)
- [ ] Finalize which charts → Altair for publication-ready PNG export
- [ ] Add @unwelcomedata watermark
- [ ] Create twitter_landscape presets where needed
- [ ] Draft social media copy for each chart

---

## 📁 KEY FILES

| File | Purpose | Status |
|------|---------|--------|
| `notebooks/04-viz.ipynb` | Exploratory charts + analysis | ✓ Complete |
| `ANALYSIS-FINDINGS.md` | Documented findings | ✓ Complete |
| `PROJECT-STATUS.md` | This file | 📝 In progress |
| `notebooks/04b-viz-social.ipynb` | Altair publication charts | 📅 Next |
| `data/project.duckdb` | DuckDB with all tables | ✓ Loaded |
| `export/abortion_cause_of_death_v1.csv` | Master comparison table | ✓ Ready |

---

## 💾 GIT HISTORY

```
1ee86fa - docs: ANALYSIS-FINDINGS.md (notable patterns)
6c12e08 - refactor: 04-viz.ipynb (stacked charts, race comparisons)
bf4a0a9 - feat: 04-viz.ipynb (initial 6 charts)
3e5a912 - chore: scaffold abortion-cause-of-death
```

---

## 🚀 SOCIAL MEDIA CAMPAIGN (DRAFT)

### Post 1: National Abortion Impact
- **Chart:** Chart 1 (national without vs. with)
- **Message:** "If abortion were a cause of death, it would rank as the 2nd-3rd leading cause in the US"
- **Hashtags:** #data #publichealth #womenshealth

### Post 2: Sex Differences in Mortality
- **Chart:** Chart 3 (stacked sex comparison)
- **Message A:** "Men are 4x more likely to die by suicide. Women are 2x more likely to die of Alzheimer's."
- **Message B:** (Individual charts for suicide and Alzheimer's if deeper dive successful)
- **Hashtags:** #mentalhealth #genderhealth #data

### Post 3: Race-Specific Abortion Impact
- **Chart:** Chart 3b (White version) + Chart 3b (Black version)
- **Message:** "How would abortion rank as a leading cause of death... if it were counted? Varies by race."
- **Hashtags:** #equity #health #data

### Post 4+: Deep Dive Findings (TBD based on explorations)
- Homicide age/race patterns
- Accident types breakdown
- "Unique cause" disparities

---

## ⚠️ LIMITATIONS & CAVEATS

1. **Perpetrator race not available in WONDER** — may require external data source
2. **Accident sub-types may not be queryable via WONDER interface** — check data cube options
3. **Age groups are 5-year bins** — not suitable for granular "peak age" analysis without sub-county query
4. **No adjustment for population size** — All numbers are raw counts, not rates per 100k
5. **Binary sex only** — WONDER data doesn't distinguish non-binary categories

---

## 📝 NOTES FOR NEXT SESSION

- Database connection: already closed properly in 04-viz.ipynb
- All display names consistently applied (DISPLAY_NAMES dict)
- Small multiples (Charts 4, 5) are exploratory—good for pattern spotting, not for social viz
- Consider creating standalone "shock" charts for:
  1. Suicide sex comparison (focused chart)
  2. Alzheimer's sex + age pattern
  3. Individual accident types (if data available)
  4. Homicide by age (if feasible)

---

**Questions for next session start:**
- Should we attempt to find perpetrator race data (NVDRS/UCR) or accept limitation?
- What's the effort to query WONDER for accident sub-types?
- How deep should we go on "unique cause" analysis (all 52 causes or top 20)?
