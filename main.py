from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle


class RestaurantRecommenderApp(App):
    def build(self):
        # Create the main layout with a background color
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with main_layout.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Set background color
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add a header with an image and title
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=5)
        header.add_widget(Image(source='assets/logo.png'))
        header.add_widget(Label(text="Welcome to Restaurant Recommender", font_size='24sp', bold=True))
        main_layout.add_widget(header)

        # Add selection bubbles for user input
        diet_options = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"]
        style_options = ["Casual", "Fine Dining", "Fast Food", "Café", "Buffet"]
        parking_options = ["Yes", "No"]
        sort_options = ["Distance", "Reviews"]

        # Create buttons for diet preferences
        main_layout.add_widget(Label(text="Select your diet preference:", font_size='20sp', bold=True))
        diet_row = BoxLayout(spacing=15, size_hint_y=None, height=60)
        for diet in diet_options:
            btn = Button(
                text=diet,
                size_hint=(None, None),
                size=(120, 60),
                background_color=(0.4, 0.7, 1, 1),
                color=(1, 1, 1, 1),
                font_size='20sp'
            )
            btn.bind(on_press=lambda instance, d=diet: self.select_option('Diet', d))
            diet_row.add_widget(btn)
        main_layout.add_widget(diet_row)

        # Create buttons for style preferences
        main_layout.add_widget(Label(text="Select your dining style:", font_size='20sp', bold=True))
        style_row = BoxLayout(spacing=15, size_hint_y=None, height=60)
        for style in style_options:
            btn = Button(
                text=style,
                size_hint=(None, None),
                size=(120, 60),
                background_color=(0.4, 0.7, 1, 1),
                color=(1, 1, 1, 1),
                font_size='20sp'
            )
            btn.bind(on_press=lambda instance, s=style: self.select_option('Style', s))
            style_row.add_widget(btn)
        main_layout.add_widget(style_row)

        # Create buttons for parking preferences
        main_layout.add_widget(Label(text="Do you need parking?:", font_size='20sp', bold=True))
        parking_row = BoxLayout(spacing=15, size_hint_y=None, height=60)
        for parking in parking_options:
            btn = Button(
                text=parking,
                size_hint=(None, None),
                size=(120, 60),
                background_color=(0.4, 0.7, 1, 1),
                color=(1, 1, 1, 1),
                font_size='20sp'
            )
            btn.bind(on_press=lambda instance, p=parking: self.select_option('Parking', p))
            parking_row.add_widget(btn)
        main_layout.add_widget(parking_row)

        # Create buttons for sorting preferences
        main_layout.add_widget(Label(text="How would you like to sort the results?:", font_size='20sp', bold=True))
        sort_row = BoxLayout(spacing=15, size_hint_y=None, height=60)
        for sort in sort_options:
            btn = Button(
                text=sort,
                size_hint=(None, None),
                size=(120, 60),
                background_color=(0.4, 0.7, 1, 1),
                color=(1, 1, 1, 1),
                font_size='20sp'
            )
            btn.bind(on_press=lambda instance, so=sort: self.select_option('Sort', so))
            sort_row.add_widget(btn)
        main_layout.add_widget(sort_row)

        # Add a styled button
        submit_button = Button(
            text='🚗 Get Recommendations',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.5, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='22sp',
            bold=True
        )
        submit_button.bind(on_press=self.get_recommendations)
        main_layout.add_widget(submit_button)

        return main_layout

    def select_option(self, category, option):
        print(f"Selected {category}: {option}")

    def get_recommendations(self, instance):
        print("Generating recommendations based on selections")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    RestaurantRecommenderApp().run()
