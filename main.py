import sys
from random import randrange

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
    # print(win.map_generator_window.chosen_nick)
    # uruchom ekrany startowe i niech one zrobia swoje w kwestiach serwera
    # niech zwracaja macierz mapy
    world_map = [[randrange(0, 4) for _ in range(40)] for _ in range(25)]
    client = "..."  # TODO Gabi: klient z twoich klas
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, world_map, client)
    window.run()
