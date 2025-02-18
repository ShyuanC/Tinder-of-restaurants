from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

class OpeningPage(App):
    def build(self):
        # Set window size if needed
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        # Create a main layout with vertical orientation
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)


        logo = Image(source='assets/logo.png', size_hint=(1, 6))
        main_layout.add_widget(logo)


        app_name_label = Label(text="Restaurant Recommender", font_size='32sp', bold=True, color=(1, 1, 1, 1))
        main_layout.add_widget(app_name_label)

        loading_label = Label(text="Loading...", font_size='20sp', italic=True, color=(0.7, 0.7, 0.7, 1))
        main_layout.add_widget(loading_label)

        # Schedule automatic transition after 3 seconds
        Clock.schedule_once(self.switch_to_main_app, 3)

        return main_layout

    def switch_to_main_app(self, dt):
        self.stop()  # Stop the current opening page app
        from main import RestaurantRecommenderApp
        RestaurantRecommenderApp().run()


if __name__ == '__main__':
    OpeningPage().run()
