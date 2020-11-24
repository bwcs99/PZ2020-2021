import sys

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidget, QLabel, QPushButton, QApplication, QHeaderView, \
    QTableWidgetItem

from . import img_gen
from server_utils.client import Client


class LobbyWindow(QMainWindow):
    """
    LobbyWindow class needs to have line transforming matrix of ints into png, also i think the best solution will be to 
    make client save map send to him by server_utils.
    """

    def __init__(self, are_you_host: bool, chosen_nick, chosen_civ, client_object=None):
        """If player is hosting game, constructor should receive True as parameter, else false"""
        super(LobbyWindow, self).__init__()
        self.players_table = None
        self.map = QLabel(self)
        self.launch_button = None
        self.init_ui(are_you_host)

        if are_you_host is True:
            self.client = Client()
            self.client.connect()
        else:
            self.client = client_object

        self.client.introduce_yourself(chosen_nick, chosen_civ)

        response = self.client.get_current_players_from_server()
        response = response.split(":")
        print(response)
        self.add_player_to_table(response)

        tmp_map = self.client.get_map_from_server()
        print(tmp_map)
        image = img_gen.get_map_overview(tmp_map)
        qim = ImageQt(image)
        new_map = QPixmap.fromImage(qim)
        self.map.setPixmap(new_map)


    def init_ui(self, are_you_host: bool):
        self.setWindowTitle("Age of Divisiveness - Game lobby")
        self.setFixedSize(1070, 630)

        self.players_table = QTableWidget(self)
        self.players_table.setGeometry(QRect(30, 30, 420, 300))
        self.players_table.setColumnCount(3)
        header = self.players_table.horizontalHeader()
        self.players_table.setHorizontalHeaderLabels(["Nickname", "Civilization", "Color"])
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.map = QLabel(self)
        self.map.setGeometry(QRect(480, 30, 570, 570))
        # TODO KRZYSZTOF also this place needs code from Krzysztof to change matrix into png
        # TODO this path should determine place where map sent by server_utils is.
        pixmap = QPixmap('/resources/images/example_map_2.png')
        self.map.setPixmap(pixmap)
        self.map.setScaledContents(True)

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
        # TODO rozpoczęcie rozgrywki czyli zamknięcie tego okna
        print("game is starting")
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LobbyWindow(True)
    win.add_player_to_table(["12", "34", "56"])
    win.show()
    sys.exit(app.exec_())
