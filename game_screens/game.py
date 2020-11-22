import arcade
from .game_view import GameView

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720


class Game(arcade.Window):
    """
    The window containing game screens.
    """
    def __init__(self, width: int, height: int, tiles: list):
        """
        :param width: Window width.
        :param height: Window height.
        :param tiles: A 2D list of integer values representing tile types.
        """
        super().__init__(width, height, "Age of Divisiveness")
        self.game_view = GameView(width, height, tiles)
        self.zoom = 0
        self.back_to_game()

    def back_to_game(self):
        """
        Returns the window to the map view.
        """
        self.show_view(self.game_view)

    def run(self):
        arcade.run()

