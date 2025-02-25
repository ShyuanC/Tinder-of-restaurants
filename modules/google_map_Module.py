import requests

def google_maps_text_search(api_key, query):
    """
    Perform a text search using Google Maps API.

    :param api_key: Your Google Maps API key.
    :param query: The search query string.
    :return: JSON response from the API or None if an error occurs.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

    """
    Get detailed information about a place using Google Maps API.

    :param api_key: Your Google Maps API key.
    :param place_id: The place ID to get details for.
    :return: JSON response from the API or None if an error occurs.
    """
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
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def get_place_info(api_key, query):
    """
    Get information about a place by performing a text search and then fetching details.

    :param api_key: Your Google Maps API key.
    :param query: The search query string.
    :return: Detailed place information or None if an error occurs.
    """
    search_results = google_maps_text_search(api_key, query)

    if search_results and search_results.get('status') == 'OK':
        first_place = search_results['results'][0]
        place_id = first_place.get('place_id')

        if place_id:
            return get_place_details(api_key, place_id)
    return None

def get_place_details(api_key, place_id):
    """
    Get detailed information about a place using Google Maps API.

    :param api_key: Your Google Maps API key.
    :param place_id: The place ID to get details for.
    :return: JSON response from the API or None if an error occurs.
    """
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
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None


if __name__ == "__main__":
    API_KEY = "AIzaSyB0hK-xReABRNcaJw4owXQDCQWrhvURoAA"  # Replace with your actual API key
    search_query = "restaurants in Sydney"

    # Get place information
    place_info = get_place_info(API_KEY, search_query)

    if place_info and place_info.get('status') == 'OK':
        place_details = place_info['result']

        # Print detailed information
        print("\nDetailed Place Information:")
        print("---------------------------")
        print(f"Name: {place_details.get('name', 'N/A')}")
        print(f"Address: {place_details.get('formatted_address', 'N/A')}")
        print(f"Phone: {place_details.get('formatted_phone_number', 'N/A')}")
        print(f"Rating: {place_details.get('rating', 'N/A')}")
        print(f"Website: {place_details.get('website', 'N/A')}")
        print(f"Price Level: {place_details.get('price_level', 'N/A')}")

        # Print opening hours if available
        if 'opening_hours' in place_details and 'weekday_text' in place_details['opening_hours']:
            print("\nOpening Hours:")
            for hours in place_details['opening_hours']['weekday_text']:
                print(hours)

        # Print reviews if available
        if 'reviews' in place_details:
            print("\nRecent Reviews:")
            for review in place_details['reviews'][:3]:  # Show first 3 reviews
                print(f"\nRating: {review.get('rating', 'N/A')} stars")
                print(f"Review: {review.get('text', 'N/A')[:200]}...")  # Show first 200 chars
                print(f"Author: {review.get('author_name', 'N/A')}")


