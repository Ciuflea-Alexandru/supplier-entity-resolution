import pandas as pd
from sqlalchemy import create_engine
from rapidfuzz import process, fuzz
import numpy as np

pd.set_option('display.max_columns', None)

print('Retrieving Data... \n')
df = pd.read_csv('presales_data_sample.csv')
pd.set_option("display.width", 10000)


def matches(row):
    score = []
    count = []
    final_score = 0.0

    def is_valid(val):
        if pd.isna(val):
            return False
        v = str(val).strip().lower()
        return v not in ['', 'none', 'null', 'n/a']

    # 1. Name Similarity
    if is_valid(row['input_company_name']) and is_valid(row['company_name']):
        name_score = fuzz.token_sort_ratio(str(row['input_company_name']).lower(), str(row['company_name']).lower())
        score.append(name_score)
        count.append(0.2)

    # 2. Country Match
    if is_valid(row['input_main_country']) and is_valid(row['main_country']):
        if str(row['input_main_country']).strip().lower() == str(row['main_country']).strip().lower():
            country_score = 100.0
        else:
            country_score = 0.0
        score.append(country_score)
        count.append(0.2)

    # 3. Region Match
    if is_valid(row['input_main_region']) and is_valid(row['main_region']):
        if str(row['input_main_region']).strip().lower() == str(row['main_region']).strip().lower():
            region_score = 100.0
        else:
            region_score = 0.0
        score.append(region_score)
        count.append(0.2)

    # 4. City Match
    if is_valid(row['input_main_city']) and is_valid(row['main_city']):
        if str(row['input_main_city']).strip().lower() == str(row['main_city']).strip().lower():
            city_score = 100.0
        else:
            city_score = 0.0
        score.append(city_score)
        count.append(0.2)

    # 5. Postcode Match
    if is_valid(row['input_main_postcode']) and is_valid(row['main_postcode']):
        if str(row['input_main_postcode']).strip().lower() == str(row['main_postcode']).strip().lower():
            postcode_score = 100.0
        else:
            postcode_score = 0.0
        score.append(postcode_score)
        count.append(0.1)

    # 6. Street Similarity
    if is_valid(row['input_main_street']) and is_valid(row['main_street']):
        street_score = fuzz.token_sort_ratio(str(row['input_main_street']).lower(), str(row['main_street']).lower())
        score.append(street_score)
        count.append(0.1)

    # Sum of active count scales to 1.0 (100%)
    total_count = sum(count)
    normalized_count = [c / total_count for c in count]

    # Calculate final score
    for s, c in zip(score, normalized_count):
        final_score += s * c

    return final_score


print('\n Printing the original data and the final score...')
df['match_score'] = df.apply(matches, axis=1)
df = df.sort_values('input_row_key', ascending=True)
print(df[['input_company_name', 'company_name', 'match_score']].head(20))

print('\n Printing the matched table...')
sorted_scores = df.groupby('input_row_key')['match_score'].idxmax()
df_matched = df.loc[sorted_scores]

print(df_matched.head(20))
df_matched.to_csv('presales_data_sample_matched.csv', index=False)
