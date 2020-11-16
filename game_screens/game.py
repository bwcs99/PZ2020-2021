import arcade
from .game_view import GameView

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720


class Game(arcade.Window):
    def __init__(self, width, height, tiles):
        super().__init__(width, height, "Age of Divisiveness")
        self.game_view = GameView(width, height, tiles)
        self.sprites = arcade.SpriteList()
        self.zoom = 0
        self.back_to_game()

    def back_to_game(self):
        self.show_view(self.game_view)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def run(self):
        arcade.run()

