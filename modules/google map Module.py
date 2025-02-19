import requests


def google_maps_text_search(api_key, query):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in text search: {e}")
        return None


def get_place_details(api_key, place_id):
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key,
        'fields': 'name,rating,formatted_phone_number,formatted_address,opening_hours,website,review,price_level'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in place details: {e}")
        return None


def main():
    API_KEY = "AIzaSyB0hK-xReABRNcaJw4owXQDCQWrhvURoAA"  # Replace with your actual API key
    search_query = "restaurants in Sydney"

    # First, perform text search
    search_results = google_maps_text_search(API_KEY, search_query)

    if search_results and search_results.get('status') == 'OK':
        # Get the first place_id from results
        first_place = search_results['results'][0]
        place_id = first_place.get('place_id')

        if place_id:
            # Get place details
            details = get_place_details(API_KEY, place_id)

            if details and details.get('status') == 'OK':
                place_info = details['result']

                # Print detailed information
                print("\nDetailed Place Information:")
                print("---------------------------")
                print(f"Name: {place_info.get('name', 'N/A')}")
                print(f"Address: {place_info.get('formatted_address', 'N/A')}")
                print(f"Phone: {place_info.get('formatted_phone_number', 'N/A')}")
                print(f"Rating: {place_info.get('rating', 'N/A')}")
                print(f"Website: {place_info.get('website', 'N/A')}")
                print(f"Price Level: {place_info.get('price_level', 'N/A')}")

                # Print opening hours if available
                if 'opening_hours' in place_info and 'weekday_text' in place_info['opening_hours']:
                    print("\nOpening Hours:")
                    for hours in place_info['opening_hours']['weekday_text']:
                        print(hours)

                # Print reviews if available
                if 'reviews' in place_info:
                    print("\nRecent Reviews:")
                    for review in place_info['reviews'][:3]:  # Show first 3 reviews
                        print(f"\nRating: {review.get('rating', 'N/A')} stars")
                        print(f"Review: {review.get('text', 'N/A')[:200]}...")  # Show first 200 chars
                        print(f"Author: {review.get('author_name', 'N/A')}")


if __name__ == "__main__":
    main()
