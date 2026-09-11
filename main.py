import pandas as pd
from sqlalchemy import create_engine
from rapidfuzz import process, fuzz
import numpy as np

# 0. CONFIGURATION & DISPLAY SETTINGS
# Ensure all columns are visible in logs
pd.set_option('display.max_columns', None)
pd.set_option("display.width", 10000)

print('Retrieving Data... \n')
df = pd.read_csv('presales_data_sample.csv')
print(f'Printing original table...\n{df.head(10)}\n')


# 1. ENTITY RESOLUTION & MATCHING ENGINE
def matches(row):
    score = []
    count = []
    final_score = 0.0

    # Check if a data value is valid
    def is_valid(val):
        if pd.isna(val):
            return False
        v = str(val).strip().lower()
        return v not in ['', 'none', 'null', 'n/a']

    # 1.1 Name Similarity(0.40%)
    if is_valid(row['input_company_name']):
        input_name = str(row['input_company_name']).lower()

        # Collect candidates name fields
        candidate_names = []
        for col in ['company_name', 'company_legal_names', 'company_commercial_names']:
            if col in row and is_valid(row[col]):
                candidate_names.append(str(row[col]).lower())

        if candidate_names:
            # Find the best name match
            name_scores = [fuzz.token_sort_ratio(input_name, c_name) for c_name in candidate_names]
            best_name_score = max(name_scores)

            score.append(best_name_score)
            count.append(0.4)

    # 1.2 Country Match(0.25%)
    if is_valid(row['input_main_country']) and is_valid(row['main_country']):
        if str(row['input_main_country']).strip().lower() == str(row['main_country']).strip().lower():
            country_score = 100.0
        else:
            country_score = 0.0
        score.append(country_score)
        count.append(0.25)

    # 1.3 Region Match(0.10%)
    if is_valid(row['input_main_region']) and is_valid(row['main_region']):
        if str(row['input_main_region']).strip().lower() == str(row['main_region']).strip().lower():
            region_score = 100.0
        else:
            region_score = 0.0
        score.append(region_score)
        count.append(0.1)

    # 1.4 City Match(0.10%)
    if is_valid(row['input_main_city']) and is_valid(row['main_city']):
        if str(row['input_main_city']).strip().lower() == str(row['main_city']).strip().lower():
            city_score = 100.0
        else:
            city_score = 0.0
        score.append(city_score)
        count.append(0.1)

    # 1.5 Postcode Match(0.075%)
    if is_valid(row['input_main_postcode']) and is_valid(row['main_postcode']):
        if str(row['input_main_postcode']).strip().lower() == str(row['main_postcode']).strip().lower():
            postcode_score = 100.0
        else:
            postcode_score = 0.0
        score.append(postcode_score)
        count.append(0.075)

    # 1.6 Street Similarity(0.075%)
    if is_valid(row['input_main_street']) and is_valid(row['main_street']):
        street_score = fuzz.token_sort_ratio(str(row['input_main_street']).lower(), str(row['main_street']).lower())
        score.append(street_score)
        count.append(0.075)

    # Sum of active count scales to 1.0(100%)
    total_count = sum(count)
    normalized_count = [c / total_count for c in count]

    # Calculate final score
    for s, c in zip(score, normalized_count):
        final_score += s * c

    return final_score


# Apply scoring function and group by input row key and select the index of the highest score
df['match_score'] = df.apply(matches, axis=1)
sorted_scores = df.groupby('input_row_key')['match_score'].idxmax()
df_matched = df.loc[sorted_scores]

# 2. PROCUREMENT DATA CURATION & EXPORT
# Filter, curate and clean columns needed for analysis
procurement_columns = [
    'input_row_key', 'veridion_id', 'company_name', 'company_legal_names',
    'main_country', 'main_country_code', 'main_region', 'main_city', 'revenue',
    'employee_count', 'year_founded', 'main_sector', 'sics_codified_industry', 'website_url'
]

df_cleaned = df_matched[procurement_columns].copy()
df_cleaned.to_csv('presales_data.csv', index=False)
print(f' Printing and exporting the cleaned table...\n{df_cleaned.head(10)}\n')


# 3. CONFIDENCE TIERING & QUALITY CONTROL(QC)
def categorize_confidence(score):
    if score < 50:
        return 'Low (< 50%) - Manual Review Needed'
    elif score <= 80:
        return 'Medium (50% - 80%) - Plausible Match'
    else:
        return 'High (> 80%) - Exact / Strong Match'


# Apply confidence categorization
df_matched['confidence_tier'] = df_matched['match_score'].apply(categorize_confidence)
counts = df_matched['confidence_tier'].value_counts()
percentages = (counts / len(df_matched) * 100).round(2)

print(f"Confidence Distribution...\n{counts}\n")
print(f"Confidence Percentages...\n{percentages}\n")
print(f"Data Quality Fill Rates (%)...\n{df_cleaned.isnull().mean() * 100}\n")

# Export the data attributes analysis reports
pd.DataFrame({'Confidence Tier': counts.index, 'Count': counts.values, 'Percentage (%)': percentages.values}) \
  .to_csv('data_attributes/confidence_analysis.csv', index=False)

pd.DataFrame({
    'Column Name': df_cleaned.columns,
    'Missing Count': df_cleaned.isnull().sum().values,
    'Fill Rate (%)': ((len(df_cleaned) - df_cleaned.isnull().sum()) / len(df_cleaned) * 100).values}) \
    .to_csv('data_attributes/data_qc_report.csv', index=False)
