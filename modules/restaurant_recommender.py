import pandas as pd
import requests

# Load cleaned restaurant data (Ensure this file exists!)
filtered_data = pd.read_csv("cleaned_yelp_data_FL.csv")

# Ensure 'categories' column contains only strings and replaces NaN with an empty string
filtered_data["categories"] = filtered_data["categories"].astype(str).fillna("").str.lower()

# API Key for ZIP Code Distance Lookup (Replace with your actual API key)
ZIPCODE_API_KEY = "5pNGaMPQMNXcIfn0nWfW3mSEt5d4kLzvTeXoxQ4ZEiPfpRVwSfsgcWaU0BakOcnJ"

class RestaurantRecommender:
    def __init__(self):
        """Initialize with an empty recommendation list and index tracker."""
        self.recommendations = []
        self.current_index = 0
        self.user_zip = None  # Store user's ZIP code

    def set_user_zip(self, zip_code):
        """Set user ZIP code from UI."""
        self.user_zip = zip_code

    def get_zip_distance(self, restaurant_zip):
        """Estimates distance between user ZIP and restaurant ZIP using an API."""
        if not self.user_zip or not restaurant_zip:
            return 9999  # ✅ Fix: Return a high number instead of "Distance unavailable"

        try:
            response = requests.get(
                f"https://www.zipcodeapi.com/rest/{ZIPCODE_API_KEY}/distance.json/{self.user_zip}/{restaurant_zip}/mile"
            )
            data = response.json()

            if "distance" in data:
                return round(data['distance'], 2)  # ✅ Fix: Ensure valid numeric output
        except requests.exceptions.RequestException:
            print("Error fetching distance from API. Using default estimate.")

        return 9999  # ✅ Fix: Ensure a numeric value is always returned

    def recommend_restaurants(self, user_diet, sort_preference="Reviews"):
        """Return a list of restaurants matching the user’s dietary preference and sorting preference."""

        # Ensure at least some data is available
        if filtered_data.empty:
            return [{"error": "No restaurants available in the dataset."}]

        # **Filtering based on user diet selection**
        matching_restaurants = filtered_data[
            filtered_data['categories'].str.contains(user_diet, case=False, na=False)
        ].copy()  # ✅ Fix: Use .copy() to avoid modifying a slice of the DataFrame

        if matching_restaurants.empty:
            return [{"error": f"No matching restaurants found for '{user_diet}'."}]

        # **Sorting Logic Based on User Preference**
        if sort_preference == "Reviews":
            # Only include restaurants with at least 30 reviews
            matching_restaurants = matching_restaurants[matching_restaurants["review_count"] >= 30]
            if matching_restaurants.empty:
                matching_restaurants = filtered_data[
                    filtered_data['categories'].str.contains(user_diet, case=False, na=False)
                ].copy()

            matching_restaurants = matching_restaurants.sort_values(
                by=["stars", "review_count", "is_open"], ascending=[False, False, False]
            )

        elif sort_preference == "Distance":
            if "postal_code" in matching_restaurants.columns:
                if not self.user_zip:
                    return [{"error": "Please enter your ZIP code first."}]

                # ✅ Fix: Use `.loc[]` to avoid `SettingWithCopyWarning`
                matching_restaurants.loc[:, "distance"] = matching_restaurants["postal_code"].apply(
                    self.get_zip_distance)

                # ✅ Fix: Convert to numeric and fill NaNs
                matching_restaurants["distance"] = pd.to_numeric(matching_restaurants["distance"],
                                                                 errors='coerce').fillna(9999)

                # ✅ Fix: Sort by distance properly
                matching_restaurants = matching_restaurants.sort_values(by="distance", ascending=True)
            else:
                return [{"error": "ZIP code data is not available in the dataset."}]

        # Convert filtered results to a list of dictionaries
        self.recommendations = matching_restaurants.to_dict(orient="records")
        self.current_index = 0  # Reset index for new recommendations

        return self.get_next_restaurant()

    def get_next_restaurant(self):
        """Return the next restaurant in the recommendation list."""
        if not self.recommendations:
            return {"error": "No recommendations available."}

        # Get current restaurant and move to the next
        restaurant = self.recommendations[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.recommendations)  # Loop over results

        # Ensure price range is shown properly
        price_range = restaurant.get("price", "N/A")

        return {
            "user_zip": f"Your ZIP Code: {self.user_zip}" if self.user_zip else "ZIP Not Available",
            "name": restaurant["name"],
            "address": f"{restaurant['address']}, {restaurant['city']}, {restaurant['state']}, {restaurant['postal_code']}",
            "stars": restaurant["stars"],
            "reviews": restaurant["review_count"],
            "categories": restaurant["categories"],
            "price": price_range,
            "distance": restaurant.get("distance", "Distance unavailable"),
            "is_open": "Open" if restaurant["is_open"] == 1 else "Closed"
        }
