import os
import sys

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QPushButton, \
    QLineEdit, QLabel

from server_utils.map_generation import generate_map
from . import img_gen
from .lobby_window import LobbyWindow
from server_utils.server import Server
from start_screens.nick_civ_window import CivCombo

import threading


class MapGeneratorWindow(QMainWindow):
    def __init__(self):
        super(MapGeneratorWindow, self).__init__()
        self.map = None
        self.generate_button = None
        self.ok_button = None
        self.seed_line = None
        self.world_map_matrix = None
        self.chosen_civ = "fat_dwarves"
        self.chosen_nick = "fat_Bob"
        self.sever = None
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
        self.seed_line.setText("Enter 6 map parameters")
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
        """ Generate world map and show its overview using 6 parameters from textflied in following order:
        height, width, seed, water quantizer, land quantizer, hills quantizer,
        Integers only, separated by ','.
        Look 'generate_map' for more info."""
        parameters = self.seed_line.text().split(',')  # array of arguments
        if len(parameters) != 6:
            self.seed_line.setText("Not enough parameters")
            return
        try:
            h = int(parameters[0])
            w = int(parameters[1])
            sd = int(parameters[2])
            p1 = int(parameters[3])
            p2 = int(parameters[4])
            p3 = int(parameters[5])
        except ValueError:
            self.seed_line.setText("Only integers allowed")
            return

        self.world_map_matrix = generate_map(height=h, width=w, params=[sd, p1, p2, p3])
        qim = ImageQt(img_gen.get_map_overview(self.world_map_matrix))
        new_map = QPixmap.fromImage(qim)
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
        self.start_server()

    def create_server_thread(self):
        # transpose the map for easier usage in game_view and server
        self.world_map_matrix = [
            [self.world_map_matrix[y][x] for y in range(len(self.world_map_matrix))]
            for x in range(len(self.world_map_matrix[0]))
        ]
        self.sever = Server(self.map)

    def start_server(self):
        # TODO BLAZEJ client-server_utils logic

        """ mapa przechowywana jest w self.world_map_matrix """
        print("Server is starting...")
        # TODO z całą pewnościa potrzebny wątek
        server_thread = threading.Thread(target=self.create_server_thread, args=())
        server_thread.start()
        self.__init_lobby_window()

    def __init_lobby_window(self):
        self.lobby_window = LobbyWindow(True, self.chosen_nick, self.chosen_civ)  # True because this is host.
        # self.lobby_window.add_player_to_table([self.chosen_nick, self.chosen_civ, "Black"])
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
