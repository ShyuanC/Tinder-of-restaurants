import requests
import random

"""⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
   PLEASE GO EASY ON MY API KEY IT WILL CHARGE MY CARD IF LIMIT IS EXCEEDED."""

GOOGLE_PLACES_API_KEY = "AIzaSyCkrHIDaoa4I_Io77RjC5rLwa9-mRVYpek"

"""PLEASE GO EASY ON MY API KEY IT WILL CHARGE MY CARD IF LIMIT IS EXCEEDED.
   ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️        """


class GoogleReviews:
    def __init__(self):
        """Initialize the GoogleReviews class with an empty cache."""
        self.places_cache = {}

    def get_place_photo(self, restaurant_name, city, state):
        """
        Fetches a random restaurant photo from Google Places API.

        Args:
            restaurant_name (str): Name of the restaurant.
            city (str): City where the restaurant is located.
            state (str): State where the restaurant is located.

        Returns:
            str: URL of a restaurant image or a placeholder if unavailable.
        """

        # Check cache to avoid redundant API calls
        if restaurant_name in self.places_cache:
            return self.places_cache[restaurant_name]

        #Search for the place
        search_url = (
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            f"?input={restaurant_name} {city} {state}"
            "&inputtype=textquery"
            "&fields=place_id"
            f"&key={GOOGLE_PLACES_API_KEY}"
        )

        response = requests.get(search_url)
        data = response.json()

        if not data.get("candidates"):
            print(f"No place found for: {restaurant_name}")
            return "assets/no_image_available.jpg"  # Local fallback image

        place_id = data["candidates"][0]["place_id"]

        #  Get place details including photos
        details_url = (
            f"https://maps.googleapis.com/maps/api/place/details/json"
            f"?place_id={place_id}"
            f"&fields=photos"
            f"&key={GOOGLE_PLACES_API_KEY}"
        )

        response = requests.get(details_url)
        data = response.json()

        if "photos" not in data.get("result", {}):
            print(f"No photos found for: {restaurant_name}")
            return "assets/no_image_available.jpg"  # Local fallback image

        photos = data["result"]["photos"]
        random_photo = random.choice(photos)  # Pick a random photo

        #photo URL
        photo_reference = random_photo["photo_reference"]
        photo_url = (
            f"https://maps.googleapis.com/maps/api/place/photo"
            f"?maxwidth=1200&photoreference={photo_reference}"
            f"&key={GOOGLE_PLACES_API_KEY}"
        )

        #Cache result
        self.places_cache[restaurant_name] = photo_url

        return photo_url

