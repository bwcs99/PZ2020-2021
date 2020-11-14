import sys

from PyQt5.QtWidgets import QApplication

from connect_window import ConnectWindow
from LobbyWindow import LobbyWindow

import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age of Divisiveness"
SCALING = 2.0

if __name__ == "__main__":

    app = QApplication(sys.argv)
    # create new start screen window
    start_screen = ConnectWindow()
    start_screen.show()

    sys.exit(app.exec_())
