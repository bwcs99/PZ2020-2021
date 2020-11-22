import os
import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QPushButton, \
    QLineEdit, QLabel

from .nick_civ_window import CivCombo
from .lobby_window import LobbyWindow


class MapGeneratorWindow(QMainWindow):
    def __init__(self):
        super(MapGeneratorWindow, self).__init__()
        self.map = None
        self.generate_button = None
        self.ok_button = None
        self.seed_line = None
        self.chosen_civ = "fat_dwarves"
        self.chosen_nick = "fat_Bob"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Map Generator")
        self.setFixedSize(800, 600)

        self.map = QLabel(self)
        self.map.setGeometry(QRect(6, 10, 781, 521))
        # Default map
        pixmap = QPixmap('resources/images/default_map.jpg')
        self.map.setPixmap(pixmap)
        self.map.setScaledContents(True)

        self.seed_line = QLineEdit(self)
        self.seed_line.setText("Enter seed.")
        self.seed_line.setGeometry(QRect(10, 550, 370, 41))

        self.generate_button = QPushButton(self)
        self.generate_button.setText("Generate")
        self.generate_button.setGeometry(QRect(390, 550, 190, 41))
        self.generate_button.clicked.connect(self.generate_map)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setGeometry(QRect(590, 550, 191, 41))
        self.ok_button.clicked.connect(self.prepare_for_game)

        self.center()
        self.show()

    def generate_map(self):
        # TODO KRZYSZTOF this function should use MapGenerator interface and set new pixmap. self.map will refresh automatically.
        seed = self.seed_line.text()  # this way you get seed_line value
        print(seed)
        new_map = QPixmap('resources/images/example_map_2.png')
        self.map.setPixmap(new_map)

    def prepare_for_game(self):
        """ When CivCombo object is created, window opens, and after closing it changes self.chosen_civ field in
        parent object by calling set_player_info method from CivCombo"""
        CivCombo(["zgredki", "elfy", "40-letnie-panny", "antysczepionkowcy"], self)  # here should be all civilizations

    def set_player_info(self, chosen_civ, chosen_nick):
        """This method ic called within CivCombo. DON'T CHANGE this function's name, even with refactor """
        self.chosen_civ = chosen_civ
        self.chosen_nick = chosen_nick

        print(self.chosen_civ, self.chosen_nick)
        self.start_game()

    def start_game(self):
        # TODO BLAZEJ client-server_utils logic
        print("Game is starting")
        # some example opening of LobbyWindow
        self.__init_lobby_window()

    def __init_lobby_window(self):
        self.lobby_window = LobbyWindow(True)
        self.lobby_window.add_player_to_table([self.chosen_nick, self.chosen_civ, "Black"])
        self.lobby_window.show()
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# for testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapGeneratorWindow()
    win.show()
    sys.exit(app.exec_())
