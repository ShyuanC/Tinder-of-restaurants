from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from modules.restaurant_recommender import RestaurantRecommender
from kivy.uix.scrollview import ScrollView
from modules.google_review import GoogleReviews
import os
import csv
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.popup import Popup
# Custom Styled Button with Rounded Corners
class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (250, 70)
        self.font_size = '22sp'
        self.color = (1, 1, 1, 1)
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.border = (20, 20, 20, 20)

        with self.canvas.before:
            Color(0.15, 0.5, 0.25, 1)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
            self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size


# Base Screen Class with Background Image
class BaseScreen(Screen):
    def __init__(self, title, options, next_screen, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = next_screen

        layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50, 50, 50])

        # Header Text
        header = Label(
            text=title,
            font_size='30sp',
            bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=1200
        )
        layout.add_widget(header)

        # Background Image
        with self.canvas.before:
            Color(1, 1, 1, 0.75)
            self.bg = Rectangle(source='assets/food.jpg',
                                pos=(0, self.height * 0.4),
                                size=(self.width, self.height * 0.25))
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Buttons
        button_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None))
        for option in options:
            btn = StyledButton(text=option)
            btn.bind(on_press=self.get_callback(option))  # FIXED: Now correctly binding button presses
            button_layout.add_widget(btn)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def get_callback(self, option):
        """Returns a function that correctly captures button press."""
        return lambda instance: self.select_option(option)

    def select_option(self, option):
        """Store the user's selection and navigate correctly."""
        print(f"User selected: {option} on screen {self.name}")

        if self.name == "diet":
            sort_screen = self.manager.get_screen("sort")
            sort_screen.user_diet = option  # Store user-selected diet
            self.manager.current = "style"  # Move to the next screen

        elif self.name == "style":
            sort_screen = self.manager.get_screen("sort")
            sort_screen.user_style = option  # Store user-selected style
            self.manager.current = "parking"

        elif self.name == "parking":
            sort_screen = self.manager.get_screen("sort")
            sort_screen.user_parking = option  # Store user-selected parking preference
            self.manager.current = "preference"

        elif self.name == "preference":
            sort_screen = self.manager.get_screen("sort")
            sort_screen.user_sort_preference = option

            if option == "Distance":
                self.manager.current = "zipcode"
            else:
                self.manager.current = "sort"

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height * 0.7)
        self.bg.size = (instance.width, instance.height * 0.3)


# Updated Prompt Screens
class DietScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("What type of food?",
                         ["Vietnamese", "Italian", "American", "Burgers", "Salad"],
                         "style", **kwargs)


class StyleScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Dining Experience?",
                         ["Casual", "Fine Dining", "Food Truck", "Sports Bar", "Cafe"],
                         "parking", **kwargs)


class ParkingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Need Parking Onsite?",
                         ["Yes", "No"],
                         "preference", **kwargs)


class PreferenceScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("What matters most for you?",
                         ["Distance", "Reviews"],
                         None, **kwargs)


class ZipCodeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50, 50, 50])

        self.label = Label(text="Enter your ZIP Code:", font_size='24sp', bold=True)
        self.layout.add_widget(self.label)

        self.zip_input = TextInput(hint_text="e.g., 32608", multiline=False, font_size='20sp')
        self.layout.add_widget(self.zip_input)

        self.submit_button = StyledButton(text="Submit")
        self.submit_button.bind(on_press=self.save_zip_code)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def save_zip_code(self, instance):
        user_zip = self.zip_input.text.strip()
        if user_zip.isdigit() and len(user_zip) == 5:
            sort_screen = self.manager.get_screen("sort")
            sort_screen.user_zip = user_zip
            sort_screen.recommender.set_user_zip(user_zip)
            self.manager.current = "sort"
        else:
            self.label.text = "Invalid ZIP Code! Please enter a 5-digit ZIP."

class SortScreen(Screen):
    CSV_FILE = "saved_restaurants.csv"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50, 50, 50])

        self.google_reviews = GoogleReviews()  # Initialize GoogleReviews API handler
        self.saved_restaurants = self.load_saved_restaurants()  # Load saved restaurants

        # Restaurant Image (Async loading)
        self.restaurant_image = AsyncImage(size_hint=(1, None), height=600)
        self.restaurant_image.bind(on_error=self.set_default_image)  # Handle image errors
        self.layout.add_widget(self.restaurant_image)

        # Wrap text inside a scrollable label
        scroll_view = ScrollView(size_hint=(1, 1))

        self.restaurant_label = Label(
            text="Fetching restaurant recommendations...",
            font_size='20sp',
            bold=True,
            halign="left",
            valign="top",
            size_hint_y=None,
            text_size=(800, None),  # Set text wrapping
        )
        self.restaurant_label.bind(texture_size=self._update_label_height)  # Adjust height dynamically
        scroll_view.add_widget(self.restaurant_label)

        self.layout.add_widget(scroll_view)

        # Add "View Added" button at the bottom-right corner
        self.view_added_button = Button(
            text="View Added",
            size_hint=(None, None),
            size=(180, 60),
            pos_hint={"right": 1, "bottom": 1}
        )
        self.view_added_button.bind(on_press=self.show_saved_restaurants)
        self.layout.add_widget(self.view_added_button)

        self.add_widget(self.layout)

        self.recommender = RestaurantRecommender()
        self.user_zip = None
        self.user_sort_preference = None
        self.user_diet = None  # Store user's food preference
        self.current_restaurant = None  # Track the currently displayed restaurant

    def _update_label_height(self, instance, size):
        """Dynamically adjust the label height based on text size."""
        instance.height = size[1]

    def on_pre_enter(self):
        """Fetch recommendations based on user input."""
        if not self.user_diet:
            self.user_diet = "Vietnamese"  # Default to avoid crashes

        if self.user_sort_preference == "Distance" and not self.user_zip:
            self.manager.current = "zipcode"
        else:
            self.recommender.recommend_restaurants(user_diet=self.user_diet, sort_preference=self.user_sort_preference)
            self.show_new_restaurant(None)

    def show_new_restaurant(self, instance):
        """Fetch and display the next restaurant recommendation."""
        recommendation = self.recommender.get_next_restaurant()
        self.current_restaurant = recommendation  # Store the current restaurant

        if "error" in recommendation:
            self.restaurant_label.text = recommendation["error"]
            self.restaurant_image.source = "assets/no_image_available.jpg"
        else:
            # Fetch image from Google Places API
            photo_url = self.google_reviews.get_place_photo(
                restaurant_name=recommendation["name"],
                city=recommendation["address"].split(",")[1].strip(),
                state=recommendation["address"].split(",")[2].strip(),
            )
            self.restaurant_image.source = photo_url  # Update restaurant image

            self.restaurant_label.text = (
                f"[b]{recommendation['name']}[/b]\n"
                f"{recommendation['address']}\n"
                f"[color=#FFD700]{recommendation['stars']} Stars[/color] ({recommendation['reviews']} Reviews)\n"
                f"[i]Price:[/i] {recommendation['price']}\n"
                f"{recommendation['categories']}\n"
                f"[size=40]Distance: {recommendation.get('distance', 'Distance Not Available')}[/size]\n"
                f"[b]{recommendation['is_open']}[/b]"
            )
            self.restaurant_label.markup = True  # Enable text markup for styling

    def on_touch_move(self, touch):
        """Detects swipe gestures."""
        if touch.dx > 50:  # Right Swipe
            self.save_restaurant()
            self.show_new_restaurant(None)
        elif touch.dx < -50:  # Left Swipe
            self.show_new_restaurant(None)
        return super().on_touch_move(touch)

    def save_restaurant(self):
        """Saves the current restaurant if not already saved."""
        if not self.current_restaurant or "error" in self.current_restaurant:
            return

        restaurant_name = self.current_restaurant["name"]

        # Check if restaurant is already saved
        if restaurant_name in self.saved_restaurants:
            print(f"{restaurant_name} is already saved.")
            return

        # Save to CSV
        with open(self.CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([restaurant_name])

        self.saved_restaurants.add(restaurant_name)  # Add to memory
        print(f"Saved: {restaurant_name}")

    def load_saved_restaurants(self):
        """Loads saved restaurants from CSV."""
        saved = set()
        if os.path.exists(self.CSV_FILE):
            with open(self.CSV_FILE, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        saved.add(row[0])
        return saved

    def show_saved_restaurants(self, instance):
        """Displays a list of saved restaurants in a popup."""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        if not self.saved_restaurants:
            label = Label(text="No restaurants saved yet.", font_size="20sp")
            content.add_widget(label)
        else:
            for name in self.saved_restaurants:
                label = Label(text=name, font_size="20sp", size_hint_y=None, height=40)
                content.add_widget(label)

        close_button = Button(text="Close", size_hint_y=None, height=50)
        popup = Popup(title="Saved Restaurants", content=content, size_hint=(None, None), size=(400, 600))
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)

        popup.open()

    def set_default_image(self, instance, error):
        """Sets a default image if loading fails."""
        print("Failed to load image, using fallback.")
        self.restaurant_image.source = "assets/no_image_available.jpg"




class RestaurantTinderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DietScreen(name='diet'))
        sm.add_widget(StyleScreen(name='style'))
        sm.add_widget(ParkingScreen(name='parking'))
        sm.add_widget(PreferenceScreen(name='preference'))
        sm.add_widget(ZipCodeScreen(name='zipcode'))
        sm.add_widget(SortScreen(name='sort'))
        sm.current = 'diet'
        return sm

if __name__ == '__main__':
    RestaurantTinderApp().run()
