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
    try:
        if win.connect_window:
            world_map = win.connect_window.lobby_window.game_map
            client = win.connect_window.client
            server_thread = None
        elif win.map_generator_window:
            world_map = win.map_generator_window.lobby_window.game_map
            client = win.map_generator_window.lobby_window.client
            server_thread = win.map_generator_window.server_thread
    except AttributeError:
        exit(1)

    if client.started:
        window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, world_map, client, server_thread)
        window.run()
