import arcade
from city import City


class CityView(arcade.View):
    def __init__(self, city: City, top_bar):
        super().__init__()
        self.city = city
        self.top_bar = top_bar
        self.buttons = arcade.SpriteList()
        self.backup = None

    def on_show(self):
        arcade.start_render()
        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.top_bar.adjust()
        img = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.buttons.draw()
        self.top_bar.draw_background()

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.backup = None

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.window.back_to_game()

