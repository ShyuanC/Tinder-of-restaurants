import pandas as pd
import requests
import random  #  For selecting 10 random restaurants

# Load and preprocess the dataset
filtered_data = pd.read_csv("cleaned_yelp_data_FL.csv")

# Ensure 'categories' column contains only strings and replaces NaN with an empty string
filtered_data["categories"] = filtered_data["categories"].astype(str).fillna("").str.lower()

# Ensure 'postal_code' is stored as a string and remove decimals if present
filtered_data["postal_code"] = filtered_data["postal_code"].astype(str).str.split('.').str[0]

# API Key for ZIP Code Distance Lookup
ZIPCODE_API_KEY = "7VsLpmFU8Hkh3ddldrrYMRMIqSAUHmzJOIS7Ig2mpSZvnC0fcSvZ3hzhmFvrSJ9Z"

class RestaurantRecommender:
    def __init__(self):
        #Initialize with an empty recommendation list, index tracker, and cache for ZIP distances.
        self.recommendations = []
        self.current_index = 0
        self.user_zip = None  # Store user's ZIP code
        self.zip_distance_cache = {}  #  Cache to store computed ZIP distances

    def set_user_zip(self, zip_code):
        #Ensure the ZIP code is a string without decimals
        self.user_zip = str(zip_code).split(".")[0]  # Convert to string and remove decimals

    def get_zip_distance(self, restaurant_zip):
        #Fetch the distance between user's ZIP and the restaurant's ZIP using an API.
        restaurant_zip = str(restaurant_zip).split(".")[0]  # Ensure ZIP is string without decimals

        if not self.user_zip or not restaurant_zip:
            return 9999  # Default large value if ZIP is missing

        # Check cache first to avoid unnecessary API calls
        if restaurant_zip in self.zip_distance_cache:
            return self.zip_distance_cache[restaurant_zip]

        try:
            response = requests.get(
                f"https://www.zipcodeapi.com/rest/{ZIPCODE_API_KEY}/distance.json/"
                f"{self.user_zip}/{restaurant_zip}/mile"
            )

            if response.status_code == 429:
                print("⚠️ Too many requests! Skipping this ZIP to avoid rate limits.") # NO MONEY SPEND PLZ
                return 9999
            if response.status_code == 200:
                print("Distance available")

            #⚠️⚠️⚠️: if user have "Distance" in their filter, only 10 results will be given due to the limitation of API usage
            #⚠️⚠️️⚠️: "Distance will be shown as "NA" if user don't choose it as a filter, again, API limitation sucks.


            data = response.json()
            if "distance" in data:
                distance = round(data['distance'], 2)
                self.zip_distance_cache[restaurant_zip] = distance  #  Cache result
                return distance
        except requests.exceptions.RequestException:
            print(f"Error fetching distance from API for ZIP {restaurant_zip}. Using default estimate.")

        return 9999

    def recommend_restaurants(self, user_diet, sort_preference="Distance"):
        #Filter restaurants based on diet, then sort by reviews or distance, returning top 10 closest places
        if filtered_data.empty:
            return [{"error": "No restaurants available in the dataset."}]

        # Filter based on user diet selection**
        matching_restaurants = filtered_data[
            filtered_data['categories'].str.contains(user_diet, case=False, na=False)
        ].copy()

        if matching_restaurants.empty:
            return [{"error": f"No matching restaurants found for '{user_diet}'."}]

        # **Step 2: Select 10 random restaurants before making API calls**
        matching_restaurants = matching_restaurants.sample(n=min(10, len(matching_restaurants)), random_state=42)

        #  Sorting Logic Based on User Preference**
        if sort_preference == "Reviews":
            # Only include restaurants with at least 30 reviews
            matching_restaurants = matching_restaurants[matching_restaurants["review_count"] >= 30]
            matching_restaurants = matching_restaurants.sort_values(
                by=["stars", "review_count", "is_open"], ascending=[False, False, False]
            )

        elif sort_preference == "Distance":
            if "postal_code" in matching_restaurants.columns:
                if not self.user_zip:
                    return [{"error": "Please enter your ZIP code first."}]

                matching_restaurants["distance"] = matching_restaurants["postal_code"].apply(
                    self.get_zip_distance
                )

                matching_restaurants["distance"] = pd.to_numeric(
                    matching_restaurants["distance"], errors='coerce'
                ).fillna(9999)

                matching_restaurants = matching_restaurants.sort_values(by="distance", ascending=True)
            else:
                return [{"error": "ZIP code data is not available in the dataset."}]

        #  Select top 10
        self.recommendations = matching_restaurants.head(10).to_dict(orient="records")
        self.current_index = 0  # Reset index for new recommendations

        return self.get_recommendations_list()

    def get_recommendations_list(self):
        if not self.recommendations:
            return [{"error": "No recommendations available."}]

        result = []
        for restaurant in self.recommendations:
            result.append({
                "name": restaurant["name"],
                "address": (
                    f"{restaurant['address']}, {restaurant['city']}, "
                    f"{restaurant['state']}, {restaurant['postal_code']}"
                ),
                "stars": restaurant["stars"],
                "reviews": restaurant["review_count"],
                "categories": restaurant["categories"],
                "price": restaurant.get("price", "N/A"),
                "distance": restaurant.get("distance", "Distance unavailable"),
                "is_open": "Open" if restaurant["is_open"] == 1 else "Closed",
                "zipcode": restaurant["postal_code"]
            })

        return result

    def get_next_restaurant(self):
        """Return the next restaurant in the recommendation list."""
        if not self.recommendations:
            return {"error": "No recommendations available."}

        # Get current restaurant and move to the next
        restaurant = self.recommendations[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.recommendations)  # Loop over results

        return {
            "user_zip": (
                f"Your ZIP Code: {self.user_zip}" if self.user_zip else "ZIP Not Available"
            ),
            "name": restaurant["name"],
            "address": f"{restaurant['address']}, {restaurant['city']}, {restaurant['state']}, {restaurant['postal_code']}",
            "city": restaurant["city"],
            "zipcode": restaurant["postal_code"],
            "address": (
                f"{restaurant['address']}, {restaurant['city']}, "
                f"{restaurant['state']}, {restaurant['postal_code']}"
            ),
            "stars": restaurant["stars"],
            "reviews": restaurant["review_count"],
            "categories": restaurant["categories"],
            "price": restaurant.get("price", "N/A"),
            "distance": restaurant.get("distance", "Distance unavailable"),
            "is_open": "Open" if restaurant["is_open"] == 1 else "Closed"
        }
