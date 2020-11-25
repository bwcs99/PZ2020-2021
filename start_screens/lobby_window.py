import ast
import sys
import threading

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidget, QLabel, QPushButton, QApplication, QHeaderView, \
    QTableWidgetItem

from server_utils.client import Client
from . import img_gen


class LobbyWindow(QMainWindow):
    """
    LobbyWindow is the biggest rogue of this app's gui.
    If you are host, client is constructed inside, if you are client it's passed to constructor.
    """

    def __init__(self, are_you_host: bool, chosen_nick, chosen_civ, client_object=None):
        """ If player is hosting game, constructor should receive True as parameter, else false. """
        super(LobbyWindow, self).__init__()
        self.players_table = None
        self.map_label = QLabel(self)
        self.launch_button = None
        self.init_ui(are_you_host)
        self.game_map = None

        self.lock = False  # this should be think over. Deeply.

        if are_you_host is True:  # if you are host, client hasn't been created yet, no it's his time
            self.client = Client()
            self.client.connect()
        else:  # if you are client, you already used client for getting available civilizations
            self.client = client_object

        self.client.introduce_yourself(chosen_nick, chosen_civ)  # this sends nick and civ to server.

        # this gets list of current players, in order to print them in player.table
        response = self.client.get_current_players_from_server()

        # response is in string, looks something like "["a:b:c","d:e:f",...]" , so it has to be evaluated
        response = ast.literal_eval(response)

        for player_string in response:
            nick, civ, col = player_string.split(":")
            self.add_player_to_table([nick, civ, col])

        # part which gets map from server (even if you are host) and evaluates it (cause it's string)
        self.game_map = self.client.get_map_from_server()
        self.game_map = ast.literal_eval(self.game_map)

        image = img_gen.get_map_overview(self.game_map).rotate(270, expand=1).transpose(Image.FLIP_LEFT_RIGHT)
        image = img_gen.get_resized_map_overview(image, 570, 570)
        qim = ImageQt(image).copy()  # this copy is to keep buffer clean
        new_map = QPixmap.fromImage(qim)
        self.map_label.setPixmap(new_map)

        """ 
        Crucial thread. 
        As long as host doesn't click LAUNCH, everyone is waiting in lobby and updating theirs player's table
        """
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
        pixmap = QPixmap('/resources/images/example_map_2.png')  # not sure if it's needed.
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
        # self.lock = True
        self.client.exit_lobby()
        # self.lock = False

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def wait_for_new_players(self, are_you_host):
        """
        This is thread method.
        It listens for new player info which is being broadcast by server.
        It's a bit wicked with sending and receiving, but for now it's ok. It's ok.
        """
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
    win = LobbyWindow(True, "fat", "zgredki")
    win.add_player_to_table(["12", "34", "56"])
    win.show()
    sys.exit(app.exec_())
