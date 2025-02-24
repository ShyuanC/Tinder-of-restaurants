"""

Sorts by stars (highest rating first) instead of review count.
 Only includes restaurants with 30+ reviews for better accuracy.
 Sorting by "Distance" still works properly.
Supports "Next Restaurant" button to cycle through multiple results.
Ensures top-rated restaurants are always recommended first.

what's more ?

"""

import pandas as pd
import geocoder
from geopy.distance import geodesic

# Load cleaned restaurant data (Ensure this file exists!)
filtered_data = pd.read_csv("D:/Tinder-of-restaurants/cleaned_yelp_data_FL.csv")


class RestaurantRecommender:
    def __init__(self):
        """Initialize with an empty recommendation list and index tracker."""
        self.recommendations = []
        self.current_index = 0
        self.user_location = None  # Initialize user location

    def get_user_location(self):
        """Returns user's latitude and longitude (auto-detect or manual input)."""
        location = geocoder.ip("me")  # Auto-detect location
        if location.latlng:
            return tuple(location.latlng)  # (latitude, longitude)

        print("Could not auto-detect location. Please enter manually.")
        lat = float(input("Enter your latitude: "))
        lon = float(input("Enter your longitude: "))
        return (lat, lon)

    def calculate_distance(self, restaurant):
        """Calculate distance between user and restaurant in miles."""
        if not self.user_location:
            self.user_location = self.get_user_location()

        restaurant_location = (restaurant["latitude"], restaurant["longitude"])
        return geodesic(self.user_location, restaurant_location).miles

    def recommend_restaurants(self, user_diet, sort_preference="Reviews"):
        """Return a list of restaurants matching the user’s dietary preference and sorting preference."""

        # Filter restaurants based on diet preference
        matching_restaurants = filtered_data[
            filtered_data['categories'].str.contains(user_diet, case=False, na=False)
        ]

        if matching_restaurants.empty:
            return [{"error": f"No matching restaurants found for {user_diet}."}]

        # **Sorting Logic Based on User Preference**
        if sort_preference == "Reviews":
            # Exclude restaurants with fewer than 30 reviews and sort by highest rating (stars)
            matching_restaurants = matching_restaurants[matching_restaurants["review_count"] >= 30]
            matching_restaurants = matching_restaurants.sort_values(
                by=["stars", "review_count", "is_open"], ascending=[False, False, False]
            )
        elif sort_preference == "Distance":
            if "latitude" in matching_restaurants.columns and "longitude" in matching_restaurants.columns:
                if not self.user_location:
                    self.user_location = self.get_user_location()

                # Compute distance for each restaurant
                matching_restaurants["distance"] = matching_restaurants.apply(self.calculate_distance, axis=1)
                matching_restaurants = matching_restaurants.sort_values(by="distance", ascending=True)
            else:
                return [{"error": "Distance data is not available in the dataset."}]

        # Ensure Open Restaurants Are Recommended First
        matching_restaurants = matching_restaurants.sort_values(by=["is_open"], ascending=False)

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
            "user_location": f"Your Location: {self.user_location}" if self.user_location else "Location Not Available",
            "name": restaurant["name"],
            "address": f"{restaurant['address']}, {restaurant['city']}, {restaurant['state']}, {restaurant['postal_code']}",
            "stars": restaurant["stars"],
            "reviews": restaurant["review_count"],
            "categories": restaurant["categories"],
            "price": price_range,
            "distance": f"{restaurant['distance']:.2f} miles" if "distance" in restaurant else "N/A",
            "is_open": "Open" if restaurant["is_open"] == 1 else "Closed"
        }


# **Test with User's Sorting Preference**
if __name__ == "__main__":
    recommender = RestaurantRecommender()
    recommender.recommend_restaurants("Vegetarian", "Distance")  # Test sorting by Distance

    # Print first 5 recommendations
    for _ in range(5):
        print(recommender.get_next_restaurant())
