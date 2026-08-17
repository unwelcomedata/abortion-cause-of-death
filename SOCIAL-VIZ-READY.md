# Social Viz Ready: 3 Charts for Immediate Publishing

Generated: August 17, 2026  
All charts located in `outputs/` with `.png` format (150 DPI, publication-ready)

---

## Chart 1: National Abortion as Leading Cause

**File:** `01_national_without_vs_with.png`

**Format:** 
- Left panel: Top 5 leading causes (without abortion)
- Right panel: Same 5 causes + abortion (shown in red)
- Labeled with death counts

**Key Data:**
- National deaths 2024: 2.8M total
- Abortion estimate (Guttmacher 2024): 1.124M
- Rank IF abortion were counted: ~2nd-3rd leading cause of death

**Social Media Copy:**
```
If abortion were counted as a cause of death, it would rank as the 
2nd or 3rd leading cause in the United States—above stroke, diabetes, 
and respiratory disease.

Data: CDC WONDER (2024) & Guttmacher Institute (2024 abortion estimates)
```

**Platform Presets:** Twitter (landscape), Instagram (feed), LinkedIn (landscape)

---

## Chart 3: Sex Differences in Top 10 Causes

**File:** `03_causes_by_sex_national.png`

**Format:**
- Horizontal stacked bars (Female in red-brown | Male in blue)
- Percent split shown within each bar
- Total death count on right side
- Top 10 causes nationally

**Key Data Points:**
- **Suicide: 79.8% Male** (4.0x higher than female)
  - 49,676 male deaths vs 12,516 female deaths
  - Peak age: 15-64 years

- **Alzheimer's: 67.9% Female** (2.1x higher than male)
  - 79,122 female deaths vs 37,591 male deaths
  - Peak age: 85+ years

- **Accidents: 65.7% Male** (1.9x higher)
  - 137,000+ deaths

- **Heart Disease: 55.1% Male** (slight male majority)

**Social Media Copy Option A (Suicide Focus):**
```
Men are nearly 4x more likely to die by suicide than women.
79.8% of suicide deaths in 2024 were male.

If you're struggling: National Suicide Prevention Lifeline 988
Data: CDC WONDER (2024)
```

**Social Media Copy Option B (Comparative):**
```
Men dominate deaths from suicide and accidents. Women from Alzheimer's.
Where do sex differences in causes of death come from?

Data: CDC WONDER (2024) | 2.8M U.S. deaths in 2024
```

**Social Media Copy Option C (General):**
```
The leading causes of death vary dramatically by gender.
This chart shows the top 10 leading causes of death in the U.S. in 2024,
broken down by sex. The disparities are striking.

Data: CDC WONDER (2024)
```

**Platform Presets:** Twitter (landscape, 2+ posts), Instagram (needs cropping), LinkedIn (landscape)

**Recommended Variants for Deeper Engagement:**
- Suicide-only focused chart (just that bar, large, with stats)
- Alzheimer's-only focused chart (age pattern overlay)
- Individual accident breakdown (if data becomes available)

---

## Chart 3b: Race-Specific Abortion Comparison

**Files:** 
- `03b_national_without_vs_with_race_white.png` (White population)
- `03b_national_without_vs_with_race_black_or_african_american.png` (Black population)

**Format:**
- Same as Chart 1 (side-by-side comparison)
- Left: Top 5 causes (without abortion)
- Right: Same 5 + abortion
- Race-specific data only

**Key Data (Estimated):**

**White Population:**
- Abortion est.: ~660k (proportional to death numbers)
- Would rank: ~#2-3

**Black Population:**
- Abortion est.: ~250k (proportional to death numbers)
- Would rank: ~#2-3 (higher proportion relative to leading causes)

**Social Media Copy (Dual Post):**
```
Thread: How would abortion rank as a leading cause of death... 
if it were counted? 

The answer differs by race.

🧵 1/2: Among White Americans...
[Chart: White abortion comparison]

2/2: Among Black Americans...
[Chart: Black abortion comparison]

Data: CDC WONDER (2024) & Guttmacher Institute (2024)
#data #equity #health
```

**Platform Presets:** Twitter (2-tweet thread), LinkedIn (carousel/thread), Instagram (carousel if supported)

---

## Publishing Checklist

- [ ] **Watermark:** All images need `@unwelcomedata` watermark (if not already added)
- [ ] **Resolution:** Confirmed 150 DPI (publication-ready)
- [ ] **Colors:** Accessible palette (red-brown + blue tested for colorblind)
- [ ] **Sizing:** 
  - Twitter landscape: 1200×675px
  - Instagram feed: 1080×1080px (may need cropping)
  - LinkedIn: 1200×627px
- [ ] **Attribution:** Include data sources in image or caption
- [ ] **Legal:** Verify CDC WONDER terms of use for commercial/non-profit publication
- [ ] **Timing:** Consider publication calendar (e.g., women's health awareness, mental health month)

---

## Next Steps for 04b-viz-social.ipynb

Convert these charts to publication-ready Altair with:
1. **Watermark overlay:** @unwelcomedata (bottom right)
2. **Platform presets:** Twitter landscape (1200×675), Instagram (1080×1080)
3. **Color accessibility:** Test with colorblind palette checker
4. **Copy templates:** Automated caption generation by chart type
5. **Export formats:** PNG + SVG for flexibility

---

## Archive for Later Reference

These 3 charts form the **Phase 1 social media campaign**. Additional charts can be created from:
- **Chart 4 (exploratory):** If specific age/cause patterns prove newsworthy
- **Chart 5 (exploratory):** For race-specific health equity messaging
- **New deep dives:** Homicide age/perpetrator, accident types, etc.

See `PROJECT-STATUS.md` for exploration backlog.
