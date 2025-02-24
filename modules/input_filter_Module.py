# input_filter_Module.py
import pandas as pd
import ast
import os

# Function to filter the Yelp dataset based on user selections
def filter_restaurants(diet, style, parking, sort_option, dataset_path=None):
    try:
        # Default dataset path relative to the project root if not provided
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cleaned_yelp_data_FL.csv')

        # Load the dataset
        df = pd.read_csv(dataset_path)

        # Filter for categories containing 'Restaurants'
        df = df[df['categories'].str.contains('Restaurants', case=False, na=False)]

        # Filter by diet preference (if 'attributes' contain specific diet-related keywords)
        if diet:
            diet_keywords = {
                "Vegetarian": "vegetarian",
                "Vegan": "vegan",
                "Gluten-Free": "gluten",
                "Keto": "keto",
                "Paleo": "paleo"
            }
            if diet in diet_keywords:
                df = df[df['attributes'].str.contains(diet_keywords[diet], case=False, na=False)]

        # Filter by dining style (searching in 'attributes' or 'categories')
        if style:
            df = df[df['attributes'].str.contains(style.lower(), case=False, na=False) |
                    df['categories'].str.contains(style, case=False, na=False)]

        # Filter by parking availability (check 'BusinessParking' in 'attributes')
        if parking.lower() == "yes":
            def has_parking(attributes):
                try:
                    attr_dict = ast.literal_eval(attributes)
                    parking_info = attr_dict.get('BusinessParking', '{}')
                    parking_dict = ast.literal_eval(parking_info)
                    return any(parking_dict.values())
                except:
                    return False

            df = df[df['attributes'].apply(has_parking)]

        # Sort the results based on user preference
        if sort_option.lower() == "distance" and 'distance' in df.columns:
            df = df.sort_values(by='distance')
        elif sort_option.lower() == "reviews":
            df = df.sort_values(by='review_count', ascending=False)

        # Extract and display restaurant name with latitude and longitude
        if not df.empty:
            recommendations = df[['name', 'latitude', 'longitude']].head(10)  # Top 10 recommendations
            print("\nRecommended Restaurants:")
            for _, row in recommendations.iterrows():
                print(f"- {row['name']} (Lat: {row['latitude']}, Lon: {row['longitude']})")
            return recommendations
        else:
            print("No matching restaurants found.")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error while filtering: {e}")
        return pd.DataFrame()

# Example usage (for testing):
filter_restaurants('Vegetarian', 'Casual', 'Yes', 'Distance')
