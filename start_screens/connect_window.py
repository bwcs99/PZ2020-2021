import os
import socket

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from .img_gen import get_map_overview

from .nick_civ_window import CivCombo
from .lobby_window import LobbyWindow
from server_utils.client import Client


class ConnectWindow(QMainWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()
        self.image_label = None
        self.text_line = None
        self.button = None
        self.chosen_civ = ''
        self.chosen_nick = ''
        self.client = Client()
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
        self.text_line.setText("127.0.0.1")  # in default this should be "type address"
        self.text_line.move(20, 20)
        self.text_line.resize(280, 40)

        self.button = QPushButton('Connect', self)
        self.button.move(20, 80)

        self.button.clicked.connect(self.on_click)

        self.__center()
        self.show()

    def on_click(self):
        host_address = self.text_line.text().strip()  # using strip() for annoying white chars surrounding address
        self.client.connect()
        available_civ = self.client.get_available_civilizations()
        civ_combo = CivCombo(available_civ)
        # try:
        #     # socket.inet_aton(host_address)  here put Błażej's code
        #     self.client.connect()
        #     QMessageBox.question(self, "", "Successfully connected", QMessageBox.Ok, QMessageBox.Ok)
        #     # client-server_utils's logic ...
        #     civ_combo = CivCombo(["zgredki", "elfy", "40-letnie-panny"],
        #                          self)  # ["zgredki", "elfy", "40-letnie-panny"] should be civ_list returned from server_utils
        #
        # except socket.error:
        #     QMessageBox.question(self, "host_address", "\"" + host_address + "\"" + " is incorrect address.",
        #                          QMessageBox.Ok,
        #                          QMessageBox.Ok)

    def set_player_info(self, chosen_civ, nickname):
        """This method ic called within CivCombo. DON'T CHANGE this function's name, even with refactor """
        self.chosen_civ = chosen_civ
        self.chosen_nick = nickname
        # print(self.chosen_civ, self.chosen_nick)
        self.describe_yourself()
    

    def describe_yourself(self):
        # TODO wyślij swoj nick i cywilizacje na serwer
        # TODO to co jest poniżej powinno być zapakowane w jedną metodę
        self.client.send_msg("ADD_NEW_PLAYER:"+self.chosen_nick +"::")
        self.client.send_msg("CHOOSE_CIVILISATION:"+self.chosen_nick+":"+self.chosen_civ+":")
        self.__init_lobby_window()

    def __init_lobby_window(self):
        current_players = self.client.get_current_players()
        self.lobby_window = LobbyWindow(False)
        for player in current_players:
            self.lobby_window. add_player_to_table(player)
        self.lobby_window.show()
        self.hide()
    
    # typical function for getting window in the middle of a screen
    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
