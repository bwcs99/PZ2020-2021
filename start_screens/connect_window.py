import os

import ast

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QLineEdit, QPushButton

from .nick_civ_window import CivCombo
from .lobby_window import LobbyWindow
from server_utils.client import Client


class ConnectWindow(QMainWindow):
    """
    This window is open only when you are client, who is connecting to server. After all it only provides field for
    typing ip address and creating Client which is afterwards passed to Lobby in constructor
    """

    def __init__(self):
        super(ConnectWindow, self).__init__()
        self.image_label = None
        self.text_line = None
        self.button = None
        self.chosen_civ = ''
        self.chosen_nick = ''
        self.client = Client()  # client may be open here
        self.lobby_window = None

        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Connect Window")

        # setting pixel art image as background
        self.image_label = QLabel(self)  # background label
        pixmap = QPixmap(os.getcwd() + '/resources/images/connect_window_background.png')  # example graphic
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.setCentralWidget(self.image_label)
        self.resize(int(pixmap.width() * 1.5), int(pixmap.height() * 1.5))

        # creating text label in the window
        # if someone would like to try to remove content of self.text_line after
        # clicking on it I strongly recommend taking some painkillers and alcohol before
        self.text_line = QLineEdit(self)
        self.text_line.setPlaceholderText("IP Address")  # in default this should be "type address"
        self.text_line.move(20, 20)
        self.text_line.resize(280, 40)

        self.port_line = QLineEdit(self)
        self.port_line.setPlaceholderText("Port")
        self.port_line.move(20, 80)
        self.port_line.resize(280, 40)

        self.button = QPushButton('Connect', self)
        self.button.move(20, 140)

        self.button.clicked.connect(self.on_click)

        self.__center()
        self.show()

    def on_click(self):
        host_address = self.text_line.text().strip()  # using strip() for annoying white chars surrounding address
        host_port = self.port_line.text().strip()
        self.client.connect(host_address, host_port)

        available_civ = self.client.get_available_civilizations()  # getting not yet chosen civilizations from server.
        #  available_civ now looks like "['a','b','c']". It's string!
        available_civ = ast.literal_eval(available_civ)  # evaluating string to list
        CivCombo(available_civ, self)  # by opening CivCombo with self it's possible to go back

    def set_player_info(self, chosen_civ, nickname):
        """This method ic called within CivCombo. DON'T CHANGE this function's name, even with refactor """
        self.chosen_civ = chosen_civ
        self.chosen_nick = nickname

        self.__init_lobby_window()

    def __init_lobby_window(self):
        self.lobby_window = LobbyWindow(False, self.chosen_nick, self.chosen_civ,
                                        self.client)  # False because it's client scenario.
        self.lobby_window.show()
        self.hide()

    # typical function for getting window in the middle of the screen
    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
