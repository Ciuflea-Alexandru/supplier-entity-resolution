import pandas as pd
from sqlalchemy import create_engine
from rapidfuzz import process, fuzz

pd.set_option('display.max_columns', None)

print('Retrieving Data... \n')
df = pd.read_csv('presales_data_sample.csv')


def matches(row):

    # 1. Name Similarity
    input_name = str(row['input_company_name']).lower()
    candidate_name = str(row['company_name']).lower()
    name_score = fuzz.token_sort_ratio(input_name, candidate_name)

    input_country = str(row['input_main_country']).strip().lower()
    candidate_country = str(row['main_country']).strip().lower()

    if input_country == candidate_country:
        country_score = 100.0
    else:
        country_score = 0

    input_region = str(row['input_main_region']).strip().lower()
    candidate_region = str(row['main_region']).strip().lower()

    if input_region != candidate_region:
        region_score = 100.0
    else:
        region_score = 0

    input_city = str(row['input_main_city']).strip().lower()
    candidate_city = str(row['main_city']).strip().lower()

    if input_city == candidate_city:
        city_score = 100.0
    else:
        city_score = 0

    input_postcode = str(row['input_main_postcode']).strip().lower()
    candidate_postcode = str(row['main_postcode']).strip().lower()

    if input_postcode == candidate_postcode:
        postcode_score = 100.0
    else:
        postcode_score = 0

    input_street = str(row['input_main_street']).strip().lower()
    candidate_street = str(row['main_street']).strip().lower()
    street_score = fuzz.token_sort_ratio(input_street, candidate_street)

    main_score = ((name_score * 0.2) + (country_score * 0.2) + (region_score * 0.2) +
                  (city_score * 0.2) + (postcode_score * 0.1) + (street_score * 0.1))
    return main_score


df['match_score'] = df.apply(matches, axis=1)
print(df[['input_company_name', 'company_name', 'match_score']].head(10))

idx = df.groupby('input_row_key')['match_score'].idxmax()
best_matches_df = df.loc[idx]

print(best_matches_df[['input_company_name', 'company_name']].head(10))
best_matches_df.to_csv('presales_data_sample_result.csv', index=False)
