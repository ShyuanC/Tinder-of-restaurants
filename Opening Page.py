from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window

class OpeningPage(App):
    def build(self):
        Window.size = (360 ,640)
        Window.clearcolor = (1, 0.71, 0.1, 0.9)

        # Create a main layout with vertical orientation
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = Image(source='assets/logo.png', size_hint=(1, 1), allow_stretch=True)
        main_layout.add_widget(logo)

        Clock.schedule_once(self.switch_to_main_app, 3)

        return main_layout

    def switch_to_main_app(self, dt):
        self.stop()
        from main import RestaurantRecommenderApp
        RestaurantRecommenderApp().run()


if __name__ == '__main__':
    OpeningPage().run()
