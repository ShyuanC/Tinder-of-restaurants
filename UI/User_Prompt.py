from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from modules.restaurant_recommender import RestaurantRecommender


# Custom Styled Button with Rounded Corners
class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (250, 70)  # Slightly larger
        self.font_size = '22sp'
        self.color = (1, 1, 1, 1)  # White text
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.border = (20, 20, 20, 20)

        with self.canvas.before:
            Color(0.15, 0.5, 0.25, 1)  # Deep green color for a modern look
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[30])
            self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size


# Base Screen Class with Fixed Text at the Top and Background Image
class BaseScreen(Screen):
    def __init__(self, title, options, next_screen, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50, 50, 50])

        # Header Text
        header = Label(
            text=title,
            font_size='30sp',
            bold=True,
            color=(0, 0, 0, 1),
            font_name="Roboto",
            size_hint=(1, None),
            height=750  # Set fixed height so image does not push it down
        )
        layout.add_widget(header)  # Add header at the top

        # Background Image
        with self.canvas.before:
            Color(1, 1, 1, 0.75)  # Semi-transparent overlay
            self.bg = Rectangle(source='D:/Tinder-of-restaurants/assets/food.jpg',
                                pos=(0, self.height * 0.4),
                                size=(self.width, self.height * 0.25))
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Buttons (Under Image)
        button_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, None))
        for option in options:
            btn = StyledButton(text=option)
            btn.bind(on_press=lambda instance, opt=option: self.select_option(opt, next_screen))
            button_layout.add_widget(btn)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def select_option(self, option, next_screen):
        print(f"Selected: {option}")
        if next_screen:
            self.manager.current = next_screen

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height * 0.7)  # Keeps image below text
        self.bg.size = (instance.width, instance.height * 0.3)  # Resizes dynamically


# Individual Screens
class DietScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Select Your Diet Preference",
                         ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"],
                         "style", **kwargs)


class StyleScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Select Your Dining Style",
                         ["Casual", "Fine Dining", "Fast Food", "Café", "Buffet"],
                         "parking", **kwargs)


class ParkingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Do You Need Parking?",
                         ["Yes", "No"],
                         "preference", **kwargs)


# **Restored Screen: "What Matters Most?"**
class PreferenceScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("What matters most?",
                         ["Distance", "Reviews"],
                         "sort", **kwargs)


class SortScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=[50, 50, 50, 50])

        # Label to display user ZIP (only shown if sorting by Distance)
        self.zip_label = Label(text="", font_size='20sp', bold=True)
        self.layout.add_widget(self.zip_label)

        # Label to display recommended restaurant
        self.restaurant_label = Label(text="Fetching recommendation...", font_size='24sp', bold=True)
        self.layout.add_widget(self.restaurant_label)

        # "Next Restaurant" Button
        self.next_button = Button(text="Next Restaurant", size_hint=(None, None), size=(250, 70))
        self.next_button.bind(on_press=self.show_new_restaurant)
        self.layout.add_widget(self.next_button)

        self.add_widget(self.layout)

        # Initialize recommender
        self.recommender = RestaurantRecommender()
        self.user_sort_preference = None
        self.user_zip = None  # Store ZIP code from UI input

    def on_pre_enter(self):
        """Check if sorting preference is Distance, then prompt for ZIP."""
        prev_screen_name = self.manager.previous()
        if prev_screen_name:
            prev_screen = self.manager.get_screen(prev_screen_name)
            if hasattr(prev_screen, "selected_option"):
                self.user_sort_preference = prev_screen.selected_option

            if self.user_sort_preference == "Distance":
                self.ask_for_zip()

    def ask_for_zip(self):
        """Popup to ask the user for their ZIP code."""
        box = BoxLayout(orientation='vertical', spacing=10, padding=20)

        label = Label(text="Enter your ZIP code:", font_size='22sp', bold=True)
        self.zip_input = TextInput(hint_text="e.g., 10001", multiline=False, font_size='20sp')

        submit_button = Button(text="Submit", size_hint=(None, None), size=(200, 50))
        submit_button.bind(on_press=self.save_zip_code)

        box.add_widget(label)
        box.add_widget(self.zip_input)
        box.add_widget(submit_button)

        self.popup = Popup(title="ZIP Code Required", content=box, size_hint=(None, None), size=(400, 250))
        self.popup.open()  # Ensure popup is forced to appear

    def save_zip_code(self, instance):
        """Save the entered ZIP code and start recommendations."""
        self.user_zip = self.zip_input.text.strip()
        self.popup.dismiss()

        if self.user_zip:
            self.recommender.set_user_zip(self.user_zip)  # Store ZIP in recommender
            self.zip_label.text = f"Your ZIP: {self.user_zip}"
            self.show_new_restaurant(None)  # Start showing recommendations

    def show_new_restaurant(self, instance):
        """Fetch and display the next restaurant recommendation."""
        if self.user_sort_preference == "Distance" and not self.user_zip:
            self.ask_for_zip()  # Ask for ZIP if sorting by distance
            return

        recommendation = self.recommender.get_next_restaurant()

        if "error" in recommendation:
            self.restaurant_label.text = recommendation["error"]
            self.zip_label.text = ""
        else:
            # Show ZIP location only if sorting by Distance
            if self.user_sort_preference == "Distance":
                self.zip_label.text = f"Your ZIP: {self.user_zip}"

            # Ensure distance is correctly displayed
            distance_display = recommendation.get("distance", "Distance Not Available")

            # Update restaurant details
            self.restaurant_label.text = (
                f"{recommendation['name']}\n"
                f"{recommendation['address']}\n"
                f"{recommendation['stars']} Stars ({recommendation['reviews']} Reviews)\n"
                f"Price: {recommendation['price']}\n"
                f"{recommendation['categories']}\n"
                f"Distance: {distance_display}\n"
                f"{recommendation['is_open']}"
            )


# App Class
class RestaurantTinderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DietScreen(name='diet'))
        sm.add_widget(StyleScreen(name='style'))
        sm.add_widget(ParkingScreen(name='parking'))
        sm.add_widget(PreferenceScreen(name='preference'))  # Restored "What Matters Most?" page
        sm.add_widget(SortScreen(name='sort'))
        sm.current = 'diet'
        return sm


if __name__ == '__main__':
    RestaurantTinderApp().run()
