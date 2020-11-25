import sys

from PyQt5.QtWidgets import QApplication

from game_screens import Game
from start_screens.welcome_window import WelcomeWindow

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WelcomeWindow()
    win.show()
    app.exec_()
    # TODO this is pretty dziadowskie im ngl
    try:
        world_map = win.connect_window.lobby_window.game_map
        client = win.connect_window.client
    except:
        world_map = win.map_generator_window.lobby_window.game_map
        client = win.map_generator_window.lobby_window.client

    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, world_map, client)
    window.run()
