from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen


class DietScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)  # Light yellow background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            # Add dimmed background image with rounded corners
            Color(1, 1, 1, 0.6)  # Dimmed overlay
            self.bg = RoundedRectangle(source='assets/food.jpg', pos=(0, layout.height/3), size=(layout.width, layout.height/3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_bg)

        layout.add_widget(Label(text="Select your diet preference", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        diet_options = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"]
        for diet in diet_options:
            btn = Button(text=diet, size_hint=(None, None), size=(220, 70), font_size='22sp', background_color=(0.2, 0.6, 0.3, 1), color=(1, 1, 1, 1))
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
        self.bg.pos = (0, instance.height/3)
        self.bg.size = (instance.width, instance.height/3)


class StyleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)  # Light yellow background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            # Add dimmed background image with rounded corners
            Color(1, 1, 1, 0.6)  # Dimmed overlay
            self.bg = RoundedRectangle(source='assets/food.jpg', pos=(0, layout.height/3), size=(layout.width, layout.height/3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_bg)

        layout.add_widget(Label(text="Select your dining style", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        style_options = ["Casual", "Fine Dining", "Fast Food", "Café", "Buffet"]
        for style in style_options:
            btn = Button(text=style, size_hint=(None, None), size=(220, 70), font_size='22sp', background_color=(0.3, 0.4, 0.6, 1), color=(1, 1, 1, 1))
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
        self.bg.pos = (0, instance.height/3)
        self.bg.size = (instance.width, instance.height/3)


class ParkingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)  # Light yellow background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            # Add dimmed background image with rounded corners
            Color(1, 1, 1, 0.6)  # Dimmed overlay
            self.bg = RoundedRectangle(source='assets/food.jpg', pos=(0, layout.height/3), size=(layout.width, layout.height/3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_rect)

        layout.add_widget(Label(text="Do you need parking?", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        parking_options = ["Yes", "No"]
        for parking in parking_options:
            btn = Button(text=parking, size_hint=(None, None), size=(220, 70), font_size='22sp', background_color=(0.4, 0.5, 0.7, 1), color=(1, 1, 1, 1))
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
        self.bg.pos = (0, instance.height/3)
        self.bg.size = (instance.width, instance.height/3)


class SortScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        with layout.canvas.before:
            Color(1, 1, 0.8, 1)  # Light yellow background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

            # Add dimmed background image with rounded corners
            Color(1, 1, 1, 0.6)  # Dimmed overlay
            self.bg = RoundedRectangle(source='assets/food.jpg', pos=(0, layout.height/3), size=(layout.width, layout.height/3), radius=[20, 20, 20, 20])
            layout.bind(size=self._update_bg, pos=self._update_rect)

        layout.add_widget(Label(text="How would you like to sort the results?", font_size='28sp', bold=True, color=(0, 0, 0, 1)))
        sort_options = ["Distance", "Reviews"]
        for sort in sort_options:
            btn = Button(text=sort, size_hint=(None, None), size=(220, 70), font_size='22sp', background_color=(0.5, 0.6, 0.7, 1), color=(1, 1, 1, 1))
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
        self.bg.pos = (0, instance.height/3)
        self.bg.size = (instance.width, instance.height/3)


class RestaurantRecommenderApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DietScreen(name='diet'))
        sm.add_widget(StyleScreen(name='style'))
        sm.add_widget(ParkingScreen(name='parking'))
        sm.add_widget(SortScreen(name='sort'))
        sm.current = 'diet'
        return sm


if __name__ == '__main__':
    RestaurantRecommenderApp().run()
