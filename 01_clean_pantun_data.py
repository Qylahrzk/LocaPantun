import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import os
 
print("=" * 80)
print("STEP 1: CLEANING PANTUN DATA")
print("=" * 80)
 
# Step 1: Read Excel file correctly
print("\n[1/10] Reading Excel file...")
file_path = 'Klasifikasi_Pantun_6_Tema_Baharu.xlsx'
 
if not os.path.exists(file_path):
    print(f"ERROR: File not found: {file_path}")
    print("Make sure file is in same directory as this script")
    exit(1)
 
try:
    df = pd.read_excel(
        file_path,
        sheet_name='Data Klasifikasi Pantun',
        skiprows=2,  # Skip metadata rows
        header=0
    )
    print(f"✓ Loaded {len(df)} rows")
except Exception as e:
    print(f"ERROR reading Excel: {e}")
    exit(1)
 
# Step 2: Clean column names
print("\n[2/10] Standardizing column names...")
print(f"Original columns: {list(df.columns)[:3]}...")
 
# Create mapping for Malay column names to English
column_mapping = {
    'No. Baru': 'pantun_id',
    'No. Asal': 'original_id',
    'Baris 1 (Pembayang)': 'line1',
    'Baris 2 (Pembayang)': 'line2',
    'Baris 3 (Isi)': 'line3',
    'Baris 4 (Isi)': 'line4',
    'Negeri': 'region',
    'Tema Baharu': 'theme'
}
 
# Rename columns
df.rename(columns=column_mapping, inplace=True)
 
# Keep only relevant columns
required_columns = ['pantun_id', 'line1', 'line2', 'line3', 'line4', 'region', 'theme']
available_columns = [col for col in required_columns if col in df.columns]
df = df[available_columns]
print(f"✓ Columns standardized: {list(df.columns)}")
 
# Step 3: Convert pantun_id to numeric
print("\n[3/10] Converting data types...")
df['pantun_id'] = pd.to_numeric(df['pantun_id'], errors='coerce')
 
# Remove rows where pantun_id is missing (these are headers/metadata)
initial_rows = len(df)
df = df.dropna(subset=['pantun_id'])
removed_rows = initial_rows - len(df)
print(f"✓ Removed {removed_rows} header/metadata rows")
print(f"✓ Remaining rows: {len(df)}")
 
# Step 4: Handle missing values in text columns
print("\n[4/10] Handling missing values...")
text_columns = ['line1', 'line2', 'line3', 'line4', 'region', 'theme']
missing_before = df[text_columns].isnull().sum().sum()
print(f"  Missing values before: {missing_before}")
 
# Fill missing with empty string
for col in text_columns:
    df[col] = df[col].fillna('')
 
missing_after = df[text_columns].isnull().sum().sum()
print(f"  Missing values after: {missing_after}")
print(f"✓ All missing values handled")
 
# Step 5: Strip whitespace from all text
print("\n[5/10] Cleaning text formatting...")
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()
    # Remove extra whitespace within text
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
print(f"✓ Text formatting cleaned")
 
# Step 6: Check for empty pantun
print("\n[6/10] Checking pantun completeness...")
df['is_complete'] = (
    (df['line1'].str.len() > 0) &
    (df['line2'].str.len() > 0) &
    (df['line3'].str.len() > 0) &
    (df['line4'].str.len() > 0)
)
complete = df['is_complete'].sum()
incomplete = (~df['is_complete']).sum()
print(f"  Complete pantun: {complete}")
print(f"  Incomplete pantun: {incomplete}")
if incomplete > 0:
    print(f"  (Will keep incomplete pantun but mark them)")
 
# Step 7: Create full_text field
print("\n[7/10] Creating full_text field...")
df['full_text'] = (
    df['line1'] + ' ' + 
    df['line2'] + '; ' + 
    df['line3'] + ' ' + 
    df['line4']
)
print(f"✓ Full text created")
 
# Step 8: Remove duplicates (keep first occurrence)
print("\n[8/10] Removing duplicates...")
before_dedup = len(df)
df = df.drop_duplicates(subset=['full_text'], keep='first')
after_dedup = len(df)
duplicates_removed = before_dedup - after_dedup
print(f"  Duplicates removed: {duplicates_removed}")
print(f"  Remaining: {after_dedup}")
 
# Step 9: Standardize theme names (handle variations)
print("\n[9/10] Standardizing theme names...")
print(f"  Unique themes before: {df['theme'].nunique()}")
print(f"  Themes found: {df['theme'].unique().tolist()}")
 
# Remove extra whitespace in theme
df['theme'] = df['theme'].str.strip()
 
print(f"  Unique themes after: {df['theme'].nunique()}")
 
# Step 10: Save cleaned data
print("\n[10/10] Saving cleaned data...")
output_file = 'pantun_cleaned.csv'
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"✓ Saved to {output_file}")
 
# Print summary
print("\n" + "=" * 80)
print("CLEANING COMPLETE - SUMMARY")
print("=" * 80)
print(f"\nFinal dataset:")
print(f"  Total pantun: {len(df)}")
print(f"  Complete pantun: {df['is_complete'].sum()}")
print(f"  Incomplete pantun: {(~df['is_complete']).sum()}")
print(f"\nTheme distribution:")
for theme in sorted(df['theme'].unique()):
    count = (df['theme'] == theme).sum()
    pct = (count / len(df)) * 100
    print(f"  {theme}: {count} ({pct:.1f}%)")
 
print(f"\nRegion distribution:")
for region in sorted(df['region'].unique())[:5]:
    count = (df['region'] == region).sum()
    print(f"  {region}: {count}")
print(f"  (... and {df['region'].nunique() - 5} more regions)")
 
print(f"\nSample pantun:")
sample = df.iloc[0]
print(f"  ID: {sample['pantun_id']}")
print(f"  Theme: {sample['theme']}")
print(f"  Text:\n    {sample['line1']}")
print(f"    {sample['line2']}\n    {sample['line3']}")
print(f"    {sample['line4']}")
 
print("\n✓ Ready for TASK 2: Preprocessing")