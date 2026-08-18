# Palette Implementation Guide — abortion-cause-of-death Project

**Date:** August 17, 2026  
**Status:** Ready for implementation

---

## Quick Summary

We've designed a muted, sophisticated color palette aligned with your @unwelcomedata brand identity. The key addition for this project is **sex comparison colors** (Male/Female) that work beautifully together.

| Demographic | Color | Hex | Purpose |
|---|---|---|---|
| **Male** | Teal | `#2A9D8F` | All male-focused segments (suicide, accidents, etc.) |
| **Female** | Muted Red | `#C1121F` | All female-focused segments (Alzheimer's, etc.) |

---

## Before You Start

1. **Approve the muted red (`#C1121F`)** or choose alternative (`#E63946` if too dark)
2. **Decide on race palette:** Use all 6 RACE_COLORS or subset?
3. **Ready to regenerate charts** after code changes

---

## Step 1: Update `shared/viz.py`

✅ **Already done.** SEX_COLORS and RACE_COLORS_EXPANDED have been added to `shared/viz.py`.

**Verify** by checking:
```python
from viz import SEX_COLORS, RACE_COLORS_EXPANDED
print(SEX_COLORS["Female"])  # Should print: #C1121F
```

---

## Step 2: Update `notebooks/04-viz.ipynb` (Exploration Layer)

### Current State
Charts use matplotlib inline colors:
```python
plt.bar(x_male, y_male, color='steelblue')
plt.bar(x_female, y_female, color='indianred')
```

### New State
Replace with brand palette:
```python
import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from viz import SEX_COLORS, RACE_COLORS_EXPANDED

# Stacked bar example
plt.bar(x, male_counts, label='Male', color=SEX_COLORS["Male"])
plt.bar(x, female_counts, bottom=male_counts, label='Female', color=SEX_COLORS["Female"])

# Race comparison example
for race in race_list:
    color = RACE_COLORS_EXPANDED.get(race, "#9CA3AF")  # fallback gray
    plt.bar(x, values[race], label=race, color=color)
```

### Charts to Update in 04-viz.ipynb

1. **Chart 3: Top 10 Causes by Sex (Stacked)**
   - Male: `#2A9D8F`
   - Female: `#C1121F`
   - Regenerate PNG and verify colors

2. **Chart 3b: Race Comparison (Abortion Impact)**
   - If only 2-3 races shown: Use RACE_COLORS_EXPANDED
   - Regenerate PNGs

3. **Any scatter plots**
   - If colored by sex: Use SEX_COLORS
   - If colored by race: Use RACE_COLORS_EXPANDED

### Code Template

```python
# At top of notebook
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent.parent / "shared"))
from viz import SEX_COLORS, RACE_COLORS_EXPANDED, PALETTE

# In chart functions
def plot_sex_comparison(data):
    fig, ax = plt.subplots()
    male_data = data[data['sex'] == 'Male']
    female_data = data[data['sex'] == 'Female']
    
    ax.bar(male_data.index, male_data.values, 
           label='Male', color=SEX_COLORS["Male"])
    ax.bar(female_data.index, female_data.values, 
           label='Female', color=SEX_COLORS["Female"])
    
    ax.legend()
    ax.set_title("By Sex", fontweight='bold', color=PALETTE["dark"])
    return fig

def plot_race_comparison(data):
    fig, ax = plt.subplots()
    for race in data['race'].unique():
        race_data = data[data['race'] == race]
        color = RACE_COLORS_EXPANDED.get(race, PALETTE["mid"])
        ax.bar(race_data.index, race_data.values, label=race, color=color)
    
    ax.legend()
    ax.set_title("By Race/Ethnicity", fontweight='bold', color=PALETTE["dark"])
    return fig
```

---

## Step 3: Regenerate Output PNGs

After updating 04-viz.ipynb with new colors:

1. **Run all cells** in `notebooks/04-viz.ipynb`
2. **Verify visual output**
   - Colors match palette hex codes
   - No clipping or oversaturation
   - Teal and Red are clearly distinct
3. **Overwrite existing PNGs** in `outputs/`

### Charts to Output

```
outputs/
├── 01_national_without_vs_with.png          (unchanged)
├── 02_causes_by_sex.png                     ← UPDATE
├── 02_female_without_vs_with.png            (unchanged)
├── 03_causes_by_sex_national.png            ← UPDATE (main focus)
├── 03_female_repro_without_vs_with.png      (unchanged)
├── 03b_national_without_vs_with_race_*.png  ← UPDATE if race colors applied
└── ... other exploration charts
```

---

## Step 4: Prepare for 04b-viz-social.ipynb (Social Export)

This is where Altair will export publication-ready PNGs with the same palette.

### Setup Altair Theme

```python
# At top of 04b-viz-social.ipynb
import sys
sys.path.insert(0, str(Path.cwd().parent.parent / "shared"))
from viz import SEX_COLORS, RACE_COLORS_EXPANDED, SOCIAL_THEME

# Altair palette config
SEX_DOMAIN = ["Male", "Female"]
SEX_RANGE = [SEX_COLORS["Male"], SEX_COLORS["Female"]]

RACE_DOMAIN = list(RACE_COLORS_EXPANDED.keys())
RACE_RANGE = list(RACE_COLORS_EXPANDED.values())
```

### Example Altair Charts

```python
# Stacked bar by sex
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("cause:N"),
    y=alt.Y("count:Q"),
    color=alt.Color("sex:N",
        scale=alt.Scale(domain=SEX_DOMAIN, range=SEX_RANGE),
        legend=alt.Legend(title="Sex")
    )
).properties(title="Top 10 Causes of Death by Sex")

# Scatter by race
chart = alt.Chart(df).mark_circle(size=80).encode(
    x=alt.X("age:Q"),
    y=alt.Y("rate:Q"),
    color=alt.Color("race:N",
        scale=alt.Scale(domain=RACE_DOMAIN, range=RACE_RANGE),
        legend=alt.Legend(title="Race/Ethnicity")
    )
).properties(title="Mortality Rates by Age & Race")
```

---

## Step 5: Quality Assurance

Before finalizing, test:

### Visual Inspection
- [ ] Colors match brand palette hex codes exactly
- [ ] Teal is clearly distinct from red (even on phone)
- [ ] All 6 race colors are visually distinguishable
- [ ] No color clipping or oversaturation

### Colorblind Safety
- [ ] Test with Coblis simulator: https://www.color-blindness.com/coblis-color-blindness-simulator/
- [ ] Deuteranopia: Teal vs Red still distinct? ✓
- [ ] Protanopia: Teal vs Red still distinct? ✓

### Grayscale Test
- [ ] Export chart to grayscale
- [ ] All segments remain visible and distinct

### Social Media
- [ ] Export to PNG
- [ ] Post test version to Instagram / X
- [ ] Verify colors render correctly on social platform

---

## File Changes Summary

| File | Change | Status |
|---|---|---|
| `shared/viz.py` | Added SEX_COLORS, RACE_COLORS_EXPANDED | ✅ Done |
| `notebooks/04-viz.ipynb` | Update color references | 📅 TODO |
| `outputs/*.png` | Regenerate with new palette | 📅 TODO |
| `notebooks/04b-viz-social.ipynb` | Apply palette to Altair charts | 📅 TODO |
| `export/abortion_cause_of_death_v1.*` | No change (codebook unaffected) | — |

---

## Troubleshooting

### Problem: Red looks too dark on social media
**Solution:** Use alternative `#E63946` (slightly brighter)
```python
SEX_COLORS = {
    "Female": "#E63946",  # Try this instead
    "Male": "#2A9D8F",
}
```

### Problem: Teal and red blend together on my display
**Solution:** Possible display calibration issue
- Test on other devices (phone, tablet, laptop)
- Check if colors are being compressed by platform
- Consider adjusting Altair theme brightness

### Problem: Python import fails
**Solution:** Verify path setup
```python
import sys
from pathlib import Path
# Project root should be 2 levels up from notebooks/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from viz import SEX_COLORS
```

---

## Next Steps

1. **Approve muted red color** (`#C1121F` vs `#E63946`)
2. **Update 04-viz.ipynb** with SEX_COLORS references
3. **Regenerate outputs/** — run all chart cells
4. **Build 04b-viz-social.ipynb** — Altair export layer
5. **Test accessibility** — colorblind simulator + grayscale
6. **Commit to git:** `chore: apply brand palette (SEX_COLORS, RACE_COLORS)`

---

## Questions?

- Which muted red? `#C1121F` (primary) or `#E63946` (alternative)?
- Should all 6 race colors be used, or subset?
- Timeline: Do this now, or after other analysis?

