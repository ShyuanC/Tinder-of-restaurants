from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
import os

# Get the current file directory
current_dir = os.path.dirname(__file__)
# Build the full path to the image in the assets folder
food_image_path = os.path.join(current_dir, '..', 'assets', 'food.jpg')

# Custom Styled Button with Rounded Corners
class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (220, 70)
        self.font_size = '22sp'
        self.color = (1, 1, 1, 1)  # White text
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.border = (16, 16, 16, 16)

        with self.canvas.before:
            Color(0.2, 0.6, 0.3, 1)  # Custom greenish color
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[25])
            self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size


class DietScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)  # Light yellow background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            # Dimmed background image with rounded corners
            Color(1, 1, 1, 0.9)
            self.bg = RoundedRectangle(source= food_image_path, pos=(0, self.height * 0.65),
                                       size=(self.width, self.height * 0.3), radius=[20, 20, 20, 20])
            self.bind(size=self._update_bg, pos=self._update_bg)

        layout.add_widget(Label(text="Select your diet preference", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        diet_options = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"]
        for diet in diet_options:
            btn = StyledButton(text=diet)
            btn.bind(on_press=lambda instance, d=diet: self.select_option(d))
            layout.add_widget(btn)
        self.add_widget(layout)

    def select_option(self, option):
        print(f"Selected Diet: {option}")
        self.manager.current = 'style'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height / 3)
        self.bg.size = (instance.width, instance.height / 3)


class StyleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            Color(1, 1, 1, 0.6)
            self.bg = RoundedRectangle(source=food_image_path, pos=(0, layout.height / 3),
                                       size=(layout.width, layout.height / 3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_bg)

        layout.add_widget(Label(text="Select your dining style", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        style_options = ["Casual", "Fine Dining", "Fast Food", "Café", "Buffet"]
        for style in style_options:
            btn = StyledButton(text=style)
            btn.bind(on_press=lambda instance, s=style: self.select_option(s))
            layout.add_widget(btn)
        self.add_widget(layout)

    def select_option(self, option):
        print(f"Selected Style: {option}")
        self.manager.current = 'parking'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height / 3)
        self.bg.size = (instance.width, instance.height / 3)


class ParkingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            Color(1, 1, 1, 0.6)
            self.bg = RoundedRectangle(source=food_image_path, pos=(0, layout.height / 3),
                                       size=(layout.width, layout.height / 3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_rect)

        layout.add_widget(Label(text="Do you need parking?", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        parking_options = ["Yes", "No"]
        for parking in parking_options:
            btn = StyledButton(text=parking)
            btn.bind(on_press=lambda instance, p=parking: self.select_option(p))
            layout.add_widget(btn)
        self.add_widget(layout)

    def select_option(self, option):
        print(f"Selected Parking: {option}")
        self.manager.current = 'sort'

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height / 3)
        self.bg.size = (instance.width, instance.height / 3)


class SortScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            Color(1, 1, 1, 0.6)
            self.bg = RoundedRectangle(source=food_image_path, pos=(0, layout.height / 3),
                                       size=(layout.width, layout.height / 3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_rect)

        layout.add_widget(Label(text="How would you like to sort the results?", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        sort_options = ["Distance", "Reviews"]
        for sort in sort_options:
            btn = StyledButton(text=sort)
            btn.bind(on_press=lambda instance, so=sort: self.select_option(so))
            layout.add_widget(btn)
        self.add_widget(layout)

    def select_option(self, option):
        print(f"Selected Sort: {option}")
        print("Generating recommendations based on selections")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_bg(self, instance, value):
        self.bg.pos = (0, instance.height / 3)
        self.bg.size = (instance.width, instance.height / 3)


class RestaurantTinderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DietScreen(name='diet'))
        sm.add_widget(StyleScreen(name='style'))
        sm.add_widget(ParkingScreen(name='parking'))
        sm.add_widget(SortScreen(name='sort'))
        sm.current = 'diet'
        return sm


if __name__ == '__main__':
    RestaurantTinderApp().run()
