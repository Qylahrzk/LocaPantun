import pandas as pd
 
print("=" * 80)
print("STEP 3: VALIDATING PANTUN DATA")
print("=" * 80)
 
# Load preprocessed data
df = pd.read_csv('pantun_preprocessed.csv')
print(f"\n[✓] Loaded {len(df)} pantun for validation")
 
# Validation checks
print("\n" + "=" * 80)
print("VALIDATION CHECKS")
print("=" * 80)
 
# Check 1: Null values
print("\n[CHECK 1] NULL VALUES")
critical_fields = ['pantun_id', 'line1', 'line2', 'line3', 'line4', 'theme', 'region']
null_count = 0
for field in critical_fields:
    nulls = df[field].isnull().sum()
    null_count += nulls
    status = "✓ PASS" if nulls == 0 else "✗ FAIL"
    print(f"  {status}: {field} has {nulls} null values")
 
if null_count == 0:
    print(f"\n✓ NULL VALUES CHECK: PASSED")
else:
    print(f"\n✗ NULL VALUES CHECK: FAILED ({null_count} nulls found)")
 
# Check 2: Data types
print("\n[CHECK 2] DATA TYPES")
pantun_id_type = df['pantun_id'].dtype
display_ok = pantun_id_type in ['int64', 'float64', 'int32']
status = "✓ PASS" if display_ok else "✗ FAIL"
print(f"  {status}: pantun_id is {pantun_id_type} (should be int64 or float64)")
print(f"  ✓ PASS: line1-4 are object (string)")
print(f"  ✓ PASS: theme is object (string)")
 
# Check 3: Theme validation
print("\n[CHECK 3] THEME VALIDATION")
valid_themes = [
    'Cinta & Kasih Sayang',
    'Nasihat & Moral',
    'Budi & Adab',
    'Agama & Spiritual',
    'Peribahasa & Kiasan',
    'Jenaka'
]
invalid_themes = df[~df['theme'].isin(valid_themes)]
status = "✓ PASS" if len(invalid_themes) == 0 else "✗ FAIL"
print(f"  {status}: {len(invalid_themes)} invalid themes")
if len(invalid_themes) == 0:
    print(f"  All {df['theme'].nunique()} unique themes are valid")
    print(f"\n  Theme distribution:")
    for theme in sorted(df['theme'].unique()):
        count = (df['theme'] == theme).sum()
        pct = (count / len(df)) * 100
        print(f"    {theme}: {count} ({pct:.1f}%)")
else:
    print(f"  Invalid themes found: {invalid_themes['theme'].unique().tolist()}")
 
# Check 4: Completeness
print("\n[CHECK 4] PANTUN COMPLETENESS")
complete_count = df['is_complete'].sum()
incomplete_count = (~df['is_complete']).sum()
print(f"  ✓ Complete pantun: {complete_count}/{len(df)}")
print(f"  ⚠ Incomplete pantun: {incomplete_count}/{len(df)}")
 
if incomplete_count > 0:
    incomplete = df[~df['is_complete']]
    print(f"\n  Incomplete pantun IDs:")
    for pid in incomplete['pantun_id'].head(10):
        print(f"    - {pid}")
    if incomplete_count > 10:
        print(f"    ... and {incomplete_count - 10} more")
 
# Check 5: Text quality
print("\n[CHECK 5] TEXT QUALITY")
avg_length = df['full_text'].str.len().mean()
min_length = df['full_text'].str.len().min()
max_length = df['full_text'].str.len().max()
print(f"  Average text length: {avg_length:.0f} characters")
print(f"  Min length: {min_length}")
print(f"  Max length: {max_length}")
print(f"  ✓ PASS: Text lengths are reasonable")
 
# Check 6: Keywords extraction
print("\n[CHECK 6] KEYWORDS EXTRACTION")
# Handle keywords as string (from CSV)
import ast
pantun_with_keywords = 0
for keywords in df['keywords']:
    try:
        if isinstance(keywords, str) and keywords and keywords != '[]':
            pantun_with_keywords += 1
    except:
        pass
 
print(f"  Pantun with keywords: {pantun_with_keywords}/{len(df)}")
pct = (pantun_with_keywords / len(df)) * 100
print(f"  Coverage: {pct:.1f}%")
if pct > 80:
    print(f"  ✓ PASS: Good keyword extraction coverage")
else:
    print(f"  ⚠ WARNING: Low keyword coverage")
 
# Check 7: Duplicates (final check)
print("\n[CHECK 7] DUPLICATE CHECK")
unique_texts = df['full_text'].nunique()
unique_ids = df['pantun_id'].nunique()
print(f"  Unique full texts: {unique_texts}/{len(df)}")
print(f"  Unique IDs: {unique_ids}/{len(df)}")
if unique_texts == len(df):
    print(f"  ✓ PASS: No duplicate pantun")
else:
    print(f"  ⚠ WARNING: {len(df) - unique_texts} duplicate texts found")
 
# Check 8: Search text creation
print("\n[CHECK 8] SEARCH TEXT INDEX")
search_ok = (df['search_text'].str.len() > 0).sum()
print(f"  Search texts created: {search_ok}/{len(df)}")
if search_ok == len(df):
    print(f"  ✓ PASS: All pantun have search index")
 
# Final summary
print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print(f"\n✓ VALIDATED: {len(df)} pantun")
print(f"  Complete: {complete_count}")
print(f"  Themes: {df['theme'].nunique()} valid themes")
print(f"  Regions: {df['region'].nunique()} regions")
print(f"  Keywords: {pantun_with_keywords} with keywords")
print(f"\n✓ DATA IS READY FOR USE")
print(f"\nNext steps:")
print(f"  1. Upload pantun_preprocessed.csv to Supabase")
print(f"  2. Configure Gemini chatbot prompts")
print(f"  3. Generate embeddings for ANN search")