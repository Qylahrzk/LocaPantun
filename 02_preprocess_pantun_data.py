import pandas as pd
import json
from datetime import datetime
 
print("=" * 80)
print("STEP 2: PREPROCESSING PANTUN DATA")
print("=" * 80)
 
# Load cleaned data
print("\n[1/10] Loading cleaned data...")
df = pd.read_csv('pantun_cleaned.csv')
print(f"✓ Loaded {len(df)} pantun")
 
# Function to extract keywords
def extract_keywords(text):
    """Extract emotional/thematic keywords from pantun"""
    keywords = []
    text_lower = text.lower()
    
    keyword_groups = {
        'love': ['cinta', 'sayang', 'kasih', 'hati', 'asmara', 'gemar'],
        'sadness': ['sedih', 'duka', 'sesal', 'rindu', 'melankol', 'susah'],
        'joy': ['gembira', 'senang', 'bahagia', 'ceria', 'suka', 'teruja'],
        'anger': ['marah', 'murka', 'kesal', 'bengis', 'gusar'],
        'fear': ['takut', 'gentar', 'ketakutan', 'gerun'],
        'hope': ['harap', 'berharap', 'pengharapan', 'impian'],
        'advice': ['harus', 'jangan', 'perlu', 'perlulah', 'hendaklah'],
        'effort': ['usaha', 'bekerja', 'tekun', 'rajin', 'giat', 'kerja'],
        'family': ['ayah', 'ibu', 'keluarga', 'anak', 'orang tua', 'ibu bapa'],
        'friendship': ['teman', 'sahabat', 'kawan', 'persahabatan', 'ukhuwah'],
        'nature': ['bunga', 'pohon', 'alam', 'laut', 'gunung', 'sungai'],
        'time': ['waktu', 'masa', 'zaman', 'hari', 'tahun', 'malam'],
        'beauty': ['cantik', 'indah', 'elok', 'manis', 'molek'],
        'wisdom': ['bijak', 'arif', 'hikmah', 'ilmu', 'kepintaran'],
        'journey': ['perjalanan', 'jauh', 'dekat', 'tujuan', 'langkah'],
    }
    
    for keyword_group, keywords_list in keyword_groups.items():
        if any(kw in text_lower for kw in keywords_list):
            keywords.append(keyword_group)
    
    return keywords
 
# Function to determine use cases
def determine_use_cases(theme):
    """Suggest when/where this pantun should be used"""
    use_case_map = {
        'Cinta & Kasih Sayang': ['romantic', 'wedding', 'affection', 'love_expression', 'proposal'],
        'Nasihat & Moral': ['advice', 'encouragement', 'wisdom', 'motivation', 'life_lesson', 'perseverance'],
        'Budi & Adab': ['etiquette', 'manners', 'virtue', 'respect', 'conduct', 'education'],
        'Agama & Spiritual': ['prayer', 'faith', 'spiritual', 'religious_reflection', 'meditation'],
        'Peribahasa & Kiasan': ['metaphor', 'proverb', 'wisdom', 'traditional_saying', 'reflection'],
        'Jenaka': ['humor', 'funny', 'joke', 'lighthearted', 'entertainment', 'celebration']
    }
    return use_case_map.get(theme, [])
 
print("\n[2/10] Extracting keywords...")
df['keywords'] = df['full_text'].apply(extract_keywords)
pantun_with_keywords = (df['keywords'].str.len() > 0).sum()
print(f"✓ Keywords extracted for {pantun_with_keywords}/{len(df)} pantun")
 
print("\n[3/10] Determining use cases...")
df['use_cases'] = df['theme'].apply(determine_use_cases)
print(f"✓ Use cases assigned to all pantun")
 
print("\n[4/10] Creating display text...")
df['display_text'] = (
    df['line1'] + '\n' +
    df['line2'] + '\n\n' +
    df['line3'] + '\n' +
    df['line4']
)
print(f"✓ Display text formatted")
 
print("\n[5/10] Creating Gemini context...")
def create_gemini_context(row):
    """Create enriched context for Gemini understanding"""
    context = f"Theme: {row['theme']} | Region: {row['region']} | Keywords: {', '.join(row['keywords'])} | Complete: {'Yes' if row['is_complete'] else 'No'}"
    return context
 
df['gemini_context'] = df.apply(create_gemini_context, axis=1)
print(f"✓ Gemini context created")
 
print("\n[6/10] Creating search text (for full-text search)...")
df['search_text'] = (
    df['full_text'] + ' ' +
    df['theme'] + ' ' +
    df['region'] + ' ' +
    df['keywords'].apply(lambda x: ' '.join(x))
).str.lower()
print(f"✓ Search text index created")
 
print("\n[7/10] Adding metadata...")
df['data_version'] = '1.0'
df['last_updated'] = datetime.now().isoformat()
df['source'] = 'Kurik Kundi Merah Saga'
df['is_verified'] = True
print(f"✓ Metadata added")
 
print("\n[8/10] Creating pantun_text field (for API responses)...")
df['pantun_text'] = df['full_text']  # For API compatibility
print(f"✓ API text field created")
 
print("\n[9/10] Reorganizing columns...")
column_order = [
    'pantun_id',
    'line1', 'line2', 'line3', 'line4',
    'full_text',
    'display_text',
    'pantun_text',
    'theme',
    'region',
    'keywords',
    'use_cases',
    'is_complete',
    'gemini_context',
    'search_text',
    'data_version',
    'source',
    'is_verified'
]
df = df[[col for col in column_order if col in df.columns]]
print(f"✓ Columns organized")
 
print("\n[10/10] Saving preprocessed data...")
output_file = 'pantun_preprocessed.csv'
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"✓ Saved to {output_file}")
 
# Print summary
print("\n" + "=" * 80)
print("PREPROCESSING COMPLETE - SUMMARY")
print("=" * 80)
print(f"\nProcessed: {len(df)} pantun")
print(f"\nSample pantun (ID={df.iloc[0]['pantun_id']}):")
sample = df.iloc[0]
print(f"\nTEXT:")
print(f"  {sample['line1']}")
print(f"  {sample['line2']}")
print(f"  {sample['line3']}")
print(f"  {sample['line4']}")
print(f"\nMETADATA:")
print(f"  Theme: {sample['theme']}")
print(f"  Region: {sample['region']}")
print(f"  Keywords: {sample['keywords']}")
print(f"  Use Cases: {sample['use_cases']}")
print(f"  Complete: {sample['is_complete']}")
 
print("\n✓ Ready for TASK 3: Validation")