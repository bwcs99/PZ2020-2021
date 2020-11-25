import sys
import ast
import threading
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidget, QLabel, QPushButton, QApplication, QHeaderView, \
    QTableWidgetItem

from server_utils.client import Client
from . import img_gen


class LobbyWindow(QMainWindow):
    """
    LobbyWindow class needs to have line transforming matrix of ints into png, also i think the best solution will be to 
    make client save map send to him by server_utils.
    """

    def __init__(self, are_you_host: bool, chosen_nick, chosen_civ, client_object=None):
        """If player is hosting game, constructor should receive True as parameter, else false"""
        super(LobbyWindow, self).__init__()
        self.players_table = None
        self.map_label = QLabel(self)
        self.launch_button = None
        self.init_ui(are_you_host)
        self.game_map = None

        self.lock = False

        if are_you_host is True:
            self.client = Client()
            self.client.connect()
        else:
            self.client = client_object

        self.client.introduce_yourself(chosen_nick, chosen_civ)

        response = self.client.get_current_players_from_server()
        response = ast.literal_eval(response)
        for player_string in response:
            nick, civ, col = player_string.split(":")
            self.add_player_to_table([nick, civ, col])

        self.game_map = self.client.get_map_from_server()
        self.game_map = ast.literal_eval(self.game_map)
        image = img_gen.get_map_overview(self.game_map)
        qim = ImageQt(image).copy()
        new_map = QPixmap.fromImage(qim)
        self.map_label.setPixmap(new_map)

        waiting_for_new_players = threading.Thread(target=self.wait_for_new_players, args=(are_you_host,))
        waiting_for_new_players.start()

    def init_ui(self, are_you_host: bool):
        self.setWindowTitle("Age of Divisiveness - Game lobby")
        self.setFixedSize(1070, 630)

        self.players_table = QTableWidget(self)
        self.players_table.setGeometry(QRect(30, 30, 420, 300))
        self.players_table.setColumnCount(3)
        header = self.players_table.horizontalHeader()
        self.players_table.setHorizontalHeaderLabels(["Nickname", "Civilization", "Color"])
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.map_label = QLabel(self)
        self.map_label.setGeometry(QRect(480, 30, 570, 570))

        # TODO this path should determine place where map sent by server_utils is.

        # TODO uncomment following block when world_map_matrix is known
        # image = img_gen.get_map_overview(world_map_matrix)  # get image overview of generated world
        # image = img_gen.get_resized_map_overview(image, 570, 570)  # (width, height)
        # qim = ImageQt(image).copy()
        # pixmap = QPixmap(qim)

        pixmap = QPixmap('/resources/images/example_map_2.png')  # and delete this after uncommenting above
        self.map_label.setPixmap(pixmap)
        self.map_label.setScaledContents(True)

        self.launch_button = QPushButton(self)
        self.launch_button.setText("Launch")
        self.launch_button.setGeometry(QRect(30, 510, 420, 90))
        if are_you_host:
            self.launch_button.setEnabled(True)
        else:
            self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.__launch_game)

    def add_player_to_table(self, information: list):
        """
        This function should appends player_table by finding "lowest" entry and inserting row after it
        Function should receive information parameter in form of [ nick_name, civ_name, color_name ] all in string
        """
        row_position = self.players_table.rowCount()
        self.players_table.insertRow(row_position)
        for i, peace in enumerate(information):
            self.players_table.setItem(row_position, i, QTableWidgetItem(peace))

    def __launch_game(self):
        # TODO "Warto się pochylić"
        self.lock = True
        self.client.exit_lobby()
        self.lock = False

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def wait_for_new_players(self, are_you_host):
        while True:
            if not self.lock:
                new_player_info = self.client.get_new_player()
                if new_player_info[0] == "FINISH":
                    break
                else:
                    self.add_player_to_table(new_player_info[1:])
        if are_you_host is True:
            self.client.start_game()
        self.close()


# for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LobbyWindow(True)
    win.add_player_to_table(["12", "34", "56"])
    win.show()
    sys.exit(app.exec_())
