import arcade

from .game_view import GameView

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720


class Game(arcade.Window):
    """
    The window containing game screens.
    """

    def __init__(self, width: int, height: int, tiles: list, client):
        """
        :param width: Window width.
        :param height: Window height.
        :param tiles: A 2D list of integer values representing tile types.
        :param client: A client object for server communication.
        """
        super().__init__(width, height, "Age of Divisiveness")
        self.client = client
        self.game_view = GameView(width, height, tiles, client)
        self.back_to_game()

    def back_to_game(self):
        """
        Returns the window to the map view.
        """
        self.show_view(self.game_view)

    def run(self):
        arcade.run()

    def on_close(self):
        if False:  # TODO i'm host
            self.client.end_game_by_host()
        else:
            self.client.disconnect()
        self.close()

