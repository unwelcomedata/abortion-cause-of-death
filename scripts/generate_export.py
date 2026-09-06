#!/usr/bin/env python
"""Generate export files for abortion-cause-of-death project."""

import sys
import os
from pathlib import Path

PROJECT = Path(__file__).parent.parent
os.chdir(PROJECT)
sys.path.insert(0, str(PROJECT))

import pandas as pd
import duckdb

from src.ingest import load_config

cfg = load_config('config.yaml')
con = duckdb.connect(cfg['settings']['duckdb_file'])

# Load data
print("Loading data from DuckDB...")
df_abortions = con.execute('SELECT * FROM abortions').df()

# Extract abortion totals.
#   national_total  — all clinician-provided abortions (used for the National and
#                     Female categories, whose mortality baselines are all-ages).
#   repro_age_total — abortions to women 15-44 (used for the Female 15-44 category,
#                     so the abortion count matches that category's age universe).
abortion_national = df_abortions[df_abortions['measure'] == 'national_total']['value'].iloc[0]
abortion_repro = df_abortions[df_abortions['measure'] == 'repro_age_total']['value'].iloc[0]

print(f"Abortion totals: National {abortion_national:,.0f} | Repro-age (15-44) {abortion_repro:,.0f}")

# Each published category pairs a mortality baseline table with the abortion total
# that matches its population universe. (category label, source table, abortion total)
CATEGORIES = [
    ('National',     'mortality_national',     abortion_national),
    ('Female',       'mortality_female',       abortion_national),
    ('Female 15-44', 'mortality_female_repro', abortion_repro),
]

# Display name mapping
display_map = {
    'Diseases of heart': 'Heart disease',
    'Malignant neoplasms': 'Cancer',
    'Chronic lower respiratory diseases': 'Respiratory disease',
    'Cerebrovascular diseases': 'Stroke',
    "Alzheimer disease": "Alzheimer's",
    'Diabetes mellitus': 'Diabetes',
    'Accidents (unintentional injuries)': 'Accidents',
    'Intentional self-harm (suicide)': 'Suicide',
    'Chronic liver disease and cirrhosis': 'Liver disease',
    'Nephritis, nephrotic syndrome and nephrosis': 'Kidney disease',
    'Influenza and pneumonia': 'Flu/Pneumonia',
    'Essential hypertension and hypertensive renal disease': 'Hypertension',
    'Assault (homicide)': 'Homicide',
    'Pregnancy, childbirth and the puerperium': 'Pregnancy/childbirth',
}

def prepare_without(df, category):
    """Prepare WITHOUT abortion table with top 10 causes."""
    result = df.head(10).copy()
    result['category'] = category
    result['scenario'] = 'Without abortion'
    result['sex'] = 'Both'
    result['gestation_group'] = None
    result['rank'] = range(1, len(result) + 1)
    result['crude_rate_adjusted'] = result['deaths'] / result['population_adjusted'] * 100_000
    
    # Map to shorter display names
    result['cause'] = result['cause'].map(display_map).fillna(result['cause'])
    
    return result[['category', 'scenario', 'rank', 'cause_code', 'cause',
                   'deaths', 'sex', 'population', 'population_adjusted',
                   'crude_rate', 'crude_rate_adjusted', 'gestation_group']]

def build_with(df_without, abortion_total, category):
    """Build WITH abortion table by adding abortion row and re-ranking."""
    df = df_without.copy()
    df['scenario'] = 'With abortion'
    
    # Create abortion row
    abortion_row = pd.DataFrame([{
        'category': category,
        'scenario': 'With abortion',
        'rank': None,
        'cause_code': 'ABORT',
        'cause': 'Abortion',
        'deaths': int(abortion_total),
        'sex': 'Female',
        'population': df['population'].iloc[0],
        'population_adjusted': df['population_adjusted'].iloc[0],
        'crude_rate': None,
        'crude_rate_adjusted': abortion_total / df['population_adjusted'].iloc[0] * 100_000,
        'gestation_group': '78.6% ≤9w, 14.2% 10-13w, 6.1% 14-20w, 1.1% ≥21w',
    }])
    
    # Combine and re-rank
    combined = pd.concat([df, abortion_row], ignore_index=True)
    combined = combined.sort_values('deaths', ascending=False).reset_index(drop=True)
    combined['rank'] = range(1, len(combined) + 1)
    
    return combined

# Build tables. The export is ordered scenario-major: all "Without abortion"
# category blocks first, then all "With abortion" blocks.
print("Building category tables (Without + With abortion)...")
without_parts, with_parts = [], []
for label, table, abortion_total in CATEGORIES:
    mort = con.execute(f'SELECT * FROM {table} ORDER BY deaths DESC').df()
    mort['population_adjusted'] = mort['population'] + abortion_total
    without = prepare_without(mort, label)
    without_parts.append(without)
    with_parts.append(build_with(without, abortion_total, label))
    print(f"  {label}: pop {mort['population'].iloc[0]:,.0f}, abortion {abortion_total:,.0f}")

# Create master table
print("Creating master export table...")
master = pd.concat(without_parts + with_parts, ignore_index=True)

master['year'] = 2024
master['data_source'] = 'CDC WONDER 2024 + Guttmacher 2024'

# Reorder columns
master = master[['year', 'category', 'scenario', 'rank', 'cause_code', 'cause',
                 'deaths', 'sex', 'population', 'population_adjusted',
                 'crude_rate', 'crude_rate_adjusted', 'gestation_group', 'data_source']]

print(f"\nMaster table: {len(master)} rows")
print(f"Categories: {master['category'].unique().tolist()}")
print(f"Scenarios: {master['scenario'].unique().tolist()}")

# Export
export_dir = Path('export')
export_dir.mkdir(exist_ok=True)

csv_file = export_dir / 'abortion_cause_of_death_v1.csv'
master.to_csv(csv_file, index=False)
print(f"✓ {csv_file.name}")

parquet_file = export_dir / 'abortion_cause_of_death_v1.parquet'
master.to_parquet(parquet_file, index=False)
print(f"✓ {parquet_file.name}")

excel_file = export_dir / 'abortion_cause_of_death_v1.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    master.to_excel(writer, sheet_name='data', index=False)
print(f"✓ {excel_file.name}")

print(f"\n✓ All files saved to: {export_dir}")

con.close()
