import arcade
from game_view import GameView

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_view = GameView(width, height)
        self.sprites = arcade.SpriteList()
        self.zoom = 0
        self.back_to_game()

    def back_to_game(self):
        self.show_view(self.game_view)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "Map Test")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
