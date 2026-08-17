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
mort_national = con.execute('SELECT * FROM mortality_national ORDER BY deaths DESC').df()
df_abortions = con.execute('SELECT * FROM abortions').df()

# Extract abortion totals
abortion_national = df_abortions[df_abortions['measure'] == 'national_total']['value'].iloc[0]

print(f"Abortion totals: National {abortion_national:,.0f}")

# Add adjusted population columns
mort_national['population_adjusted'] = mort_national['population'] + abortion_national

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

# Build tables
print("Building WITHOUT tables...")
without_national = prepare_without(mort_national, 'National')

print("Building WITH tables...")
with_national = build_with(without_national, abortion_national, 'National')

# Create master table
print("Creating master export table...")
master = pd.concat([without_national, with_national],
                   ignore_index=True)

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
    master.to_excel(writer, sheet_name='National', index=False)
print(f"✓ {excel_file.name}")

print(f"\n✓ All files saved to: {export_dir}")

con.close()
