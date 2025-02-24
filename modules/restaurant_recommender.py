import pandas as pd
import requests

# Load cleaned restaurant data (Ensure this file exists!)
filtered_data = pd.read_csv("D:/Tinder-of-restaurants/cleaned_yelp_data_FL.csv")

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
        if not self.user_zip:
            return "Distance unavailable"

        # Call ZIP Code Distance API
        try:
            response = requests.get(
                f"https://www.zipcodeapi.com/rest/{ZIPCODE_API_KEY}/distance.json/{self.user_zip}/{restaurant_zip}/mile"
            )
            data = response.json()

            if "distance" in data:
                return f"Within {round(data['distance'] / 10) * 10} miles"  # Round to nearest 10 miles
        except requests.exceptions.RequestException:
            print("Error fetching distance from API. Using default estimate.")

        return "Distance unavailable"

    def recommend_restaurants(self, user_diet, sort_preference="Reviews"):
        """Return a list of restaurants matching the user’s dietary preference and sorting preference."""

        # Filter restaurants based on diet preference
        matching_restaurants = filtered_data[
            filtered_data['categories'].str.contains(user_diet, case=False, na=False)
        ]

        if matching_restaurants.empty:
            return [{"error": f"No matching restaurants found for {user_diet}."}]

        if sort_preference == "Reviews":
            # **Fix: Ensure at least some restaurants are shown**
            matching_restaurants = matching_restaurants[matching_restaurants["review_count"] >= 30]
            if matching_restaurants.empty():  # Fallback to show at least some results
                matching_restaurants = filtered_data[
                    filtered_data['categories'].str.contains(user_diet, case=False, na=False)]

            matching_restaurants = matching_restaurants.sort_values(
                by=["stars", "review_count", "is_open"], ascending=[False, False, False]
            )

        elif sort_preference == "Distance":
            if "postal_code" in matching_restaurants.columns:
                if not self.user_zip:
                    return [{"error": "Please enter your ZIP code first."}]

                # Compute ZIP-based distance
                matching_restaurants["distance"] = matching_restaurants["postal_code"].apply(self.get_zip_distance)

                # **Fix: Sort by distance properly**
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

        # Add price range if available
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
