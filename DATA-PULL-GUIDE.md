# Manual Data Pull Guide — Supplemental Cause-of-Death Detail

These queries will give us the breakdown of **how** people die within the
Accidents, Suicide, and Homicide categories — by sex and race.

Once you've downloaded the TSV files, drop them in `data/raw/` and I'll handle
ingestion into DuckDB, cleaning, and chart integration.

---

## What we're getting

| Query | What it tells us | Chart use |
|---|---|---|
| 1. Accidents by mechanism × sex | Poisoning vs motor vehicle vs falls vs drowning | Annotate "Accidents" bar |
| 2. Suicide by method × sex | Firearms vs hanging vs poisoning | Annotate "Suicide" bar |
| 3. Homicide by method × sex × race | Firearms vs other, by demographics | Annotate "Homicide" bar |
| 4. FBI SHR victim-offender | Who kills whom (relationship + race) | Separate supplemental chart |

Queries 1–3 are all from CDC WONDER (same interface you've used before).
Query 4 is from the FBI Crime Data Explorer (different site, different process).

---

## Query 1: Accident Subtypes by Sex

**URL:** https://wonder.cdc.gov/ucd-icd10-expanded.html

**Steps:**

1. Open the URL above. Accept the data use agreement.

2. **Section 1 — Group Results By:**
   - Row 1: `ICD-10 113 Cause List`
   - Row 2: `Sex`
   - Leave Row 3 blank

3. **Section 2 — Location:** Leave as "All" (national)

4. **Section 3 — Demographics:**
   - Year: select `2024` only
   - Leave all other filters at default (all ages, all races, all sexes)

5. **Section 4 — Cause of Death:**
   - Under "ICD-10 113 Cause List", expand **Accidents (unintentional injuries)**
   - Select ALL subcategories:
     - `Transport accidents (V01-V99,Y85)`
     - `Motor vehicle accidents (V02-V04...)`
     - `Other land transport accidents (V01,V05-V06...)`
     - `Water, air and space, and other transport accidents (V90-V99,Y85)`
     - `Nontransport accidents (W00-X59,Y86)`
     - `Falls (W00-W19)`
     - `Accidental discharge of firearms (W32-W34)`
     - `Accidental drowning and submersion (W65-W74)`
     - `Accidental exposure to smoke, fire and flames (X00-X09)`
     - `Accidental poisoning and exposure to noxious substances (X40-X49)`
     - `Other and unspecified nontransport accidents (W20-W31,W35-W64,W75-W99,X10-X39,X50-X59,Y86)`
   - Also keep the **parent** `#Accidents (unintentional injuries) (V01-X59,Y85-Y86)` selected as a check

6. **Section 5 — Other Options:**
   - Check: "Show Totals"
   - Check: "Export Results"
   - Leave precision at default

7. Click **Send** → **Export** → Save as TSV

**Save as:** `data/raw/wonder_accidents_by_sex_2024.tsv`

---

## Query 2: Suicide Method by Sex

**URL:** https://wonder.cdc.gov/ucd-icd10-expanded.html

**Steps:**

1. Open URL, accept agreement.

2. **Section 1 — Group Results By:**
   - Row 1: `ICD-10 113 Cause List`
   - Row 2: `Sex`

3. **Section 3 — Demographics:** Year = `2024`

4. **Section 4 — Cause of Death:**
   - Expand **Intentional self-harm (suicide)**
   - Select ALL subcategories:
     - `Intentional self-harm (suicide) by discharge of firearms (X72-X74)`
     - `Intentional self-harm (suicide) by other and unspecified means (*U03,X60-X71,X75-X84,Y87.0)`
   - Also keep the parent `#Intentional self-harm (suicide)` selected

5. **Section 5:** Show Totals, Export Results

6. Click **Send** → **Export** → Save as TSV

**Save as:** `data/raw/wonder_suicide_by_method_sex_2024.tsv`

---

## Query 3: Homicide Method by Sex × Race

**URL:** https://wonder.cdc.gov/ucd-icd10-expanded.html

**Steps:**

1. Open URL, accept agreement.

2. **Section 1 — Group Results By:**
   - Row 1: `ICD-10 113 Cause List`
   - Row 2: `Single Race 6`
   - Row 3: `Sex`

3. **Section 3 — Demographics:** Year = `2024`

4. **Section 4 — Cause of Death:**
   - Expand **Assault (homicide)**
   - Select ALL subcategories:
     - `Assault (homicide) by discharge of firearms (*U01.4,X93-X95)`
     - `Assault (homicide) by other and unspecified means (*U01.0-*U01.3,*U01.5-*U01.9,*U02,X85-X92,X96-Y09,Y87.1)`
   - Also keep the parent `#Assault (homicide)` selected

5. **Section 5:** Show Totals, Export Results

6. Click **Send** → **Export** → Save as TSV

**Save as:** `data/raw/wonder_homicide_by_method_race_sex_2024.tsv`

---

## Query 4: FBI Supplementary Homicide Reports (Victim-Offender Data)

This is **not from WONDER**. The best source is the **Murder Accountability Project** (MAP),
which publishes cleaned case-level FBI Supplementary Homicide Report data as a CSV download.

**URL:** https://www.murderdata.org/p/data-docs.html

**Steps:**

1. Go to the URL above.

2. Find the paragraph that starts with: "To download the case-level data from
   Supplementary Homicide Report..."

3. Click the **CSV** link in that paragraph. This downloads the MAP-enhanced SHR
   dataset (case-level records, 1976–present, ~137 MB).
   - Updated: August 18, 2026
   - Includes ~39,000 additional records obtained via FOIA that FBI doesn't publish

4. The file has **31 variables per case** including:
   - `VicRace` / `OfRace` — victim and offender race
   - `VicSex` / `OfSex` — victim and offender sex
   - `VicAge` / `OfAge` — victim and offender age
   - `Weapon` — firearm type, knife, blunt object, etc.
   - `Relationship` — stranger, acquaintance, wife, husband, friend, etc.
   - `Circumstance` — argument, robbery, gang, drug-related, etc.
   - `Year`, `Month`, `State`, `Agency`

5. Also download the **data dictionary** (link on same page) for column definitions.

**Save as:** `data/raw/map_shr_case_level.csv`

**What we get from this:**
- Victim race × offender race cross-tab (who kills whom)
- Victim-offender relationship breakdown
- Weapon type detail (supplements WONDER's firearms vs other)
- Circumstance (argument, robbery, gang-related, etc.)
- Can filter to 2024 or most recent year to match our WONDER data

**Note:** FBI data has known underreporting issues (not all agencies submit to SHR).
MAP includes FOIA-obtained records to partially fill gaps. We'll note coverage in any chart.

**Alternative (if you only want aggregates):** The FBI Crime Data Explorer at
https://cde.ucr.cjis.gov only provides chart-level exports (like the offender race
CSV you already downloaded). The murderdata.org file is the raw case-level version
of the same underlying data.

---

## Query 5 (Optional): Overdose Detail by Drug Type

If you want to break down the "Accidental poisoning" category further (fentanyl vs heroin vs meth vs prescription), that requires a **Multiple Cause of Death** query instead of Underlying Cause.

**URL:** https://wonder.cdc.gov/mcd-icd10-expanded.html (different form!)

**Steps:**

1. Open the Multiple Cause of Death form.

2. **Section 1 — Group Results By:**
   - Row 1: `Multiple Cause of Death` (this is the drug-specific ICD-10 code)
   - Row 2: `Sex`

3. **Section 3 — Demographics:** Year = `2024` (or most recent available)

4. **Section 4 — Underlying Cause of Death:**
   - Filter to: `X40-X49` (Accidental poisoning) as the underlying cause

5. **Section 6 — Multiple Cause of Death:**
   - Select the specific drug codes:
     - `T40.1` — Heroin
     - `T40.2` — Other opioids (prescription)
     - `T40.3` — Methadone
     - `T40.4` — Synthetic opioids (fentanyl)
     - `T40.5` — Cocaine
     - `T43.6` — Psychostimulants (meth/amphetamines)
   - Note: A single death can have multiple drug codes (poly-drug)

6. Export as TSV.

**Save as:** `data/raw/wonder_overdose_drugs_by_sex_2024.tsv`

**Note:** This query may hit WONDER's suppression rules (cells with <10 deaths are suppressed). If so, try without the sex grouping first to get national drug-type totals.

---

## After You Download

Drop all files in `data/raw/` and let me know. I'll:

1. Ingest each TSV into DuckDB (strip WONDER footer, cast types)
2. Clean and standardize (match the existing table naming conventions)
3. Compute per-capita rates where applicable
4. Add to `_sources` metadata table
5. Build annotations or sub-charts for the side-by-side bars

---

## Priority Order

| # | Query | Effort | Impact |
|---|---|---|---|
| 1 | Suicide by method × sex | 2 min | High — "56% firearms" is a powerful annotation |
| 2 | Homicide by method × race × sex | 2 min | High — firearms % by race tells a clear story |
| 3 | Accidents by mechanism × sex | 2 min | Medium — "38% poisoning (overdoses)" reframes "Accidents" |
| 4 | FBI SHR | 10 min | Medium — perpetrator data is unique but more complex |
| 5 | Overdose drug detail | 5 min | Low priority — deep cut, good for thread content |

Queries 1-3 can all be done in ~10 minutes total from the same WONDER session.
