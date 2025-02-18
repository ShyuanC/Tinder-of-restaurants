def get_user_preferences():
    print("Welcome to the Restaurant Recommender!")

    # Get cuisine preference
    cuisine = input("Enter your preferred cuisine (e.g., Italian, Chinese, Mexican, etc.): ")

    # Get dietary restrictions
    dietary_restrictions = input("Enter any dietary restrictions (e.g., vegetarian, keto, gluten-free, or 'none'): ")

    # Get distance priority
    distance_priority = input("Would you like to sort restaurants by distance or reviews? (distance/reviews): ").strip().lower()
    while distance_priority not in ['distance', 'reviews']:
        print("Invalid input. Please enter 'distance' or 'reviews'.")
        distance_priority = input("Would you like to sort restaurants by distance or reviews? (distance/reviews): ").strip().lower()

    # Get parking preference
    parking_preference = input("Do you need parking? (yes/no): ").strip().lower()
    while parking_preference not in ['yes', 'no']:
        print("Invalid input. Please enter 'yes' or 'no'.")
        parking_preference = input("Do you need parking? (yes/no): ").strip().lower()

    # Compile preferences into a dictionary
    preferences = {
        "cuisine": cuisine,
        "dietary_restrictions": dietary_restrictions,
        "distance_priority": distance_priority,
        "parking_preference": parking_preference
    }

    print("Preferences recorded successfully!")
    return preferences


# Example usage
if __name__ == "__main__":
    user_preferences = get_user_preferences()
    print(user_preferences)
