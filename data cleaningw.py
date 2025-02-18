import json
import pandas as pd


def clean_yelp_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Filter by state (FL), stars >= 3.0, and is_open = 1
    filtered_df = df[(df['state'] == 'FL') & (df['stars'] >= 3.0) & (df['is_open'] == 1)]

    # Select relevant columns
    selected_columns = [
        'business_id', 'name', 'address', 'city', 'state', 'postal_code',
        'latitude', 'longitude', 'stars', 'review_count', 'is_open',
        'attributes', 'categories', 'hours'
    ]
    filtered_df = filtered_df[selected_columns]

    # Extract parking information if available
    def extract_parking(attributes):
        if attributes and 'BusinessParking' in attributes:
            try:
                parking_info = json.loads(attributes['BusinessParking'].replace("'", '"'))
                return ', '.join([k for k, v in parking_info.items() if v])
            except Exception as e:
                return 'N/A'
        return 'N/A'

    filtered_df['parking'] = filtered_df['attributes'].apply(extract_parking)

    # Save cleaned data
    filtered_df.to_csv(output_file, index=False)

    print(f"Cleaned data saved to {output_file}")


# Usage
clean_yelp_data('yelp_academic_dataset_business.json', 'cleaned_yelp_data_FL.csv')
