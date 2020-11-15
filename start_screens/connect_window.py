import socket
from time import sleep

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox

from start_screens.nick_civ_window import CivCombo


class ConnectWindow(QMainWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()
        self.image_label = None
        self.text_line = None
        self.button = None
        self.chosen_civ = "default_elves"
        self.chosen_nick = "default_Eve"

        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Connect Window")

        # setting pixel art image as background
        self.image_label = QLabel(self)  # background label
        pixmap = QPixmap('images/connect_window_background.png')  # example graphic
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

    def set_player_info(self, chosen_civ, nickname):
        """This method ic called within CivCombo. DON'T CHANGE this function's name, even with refactor """
        self.chosen_civ = chosen_civ
        self.chosen_nick = nickname

        print(self.chosen_civ, self.chosen_nick)
        self.start_game()

    def start_game(self):
        # TODO client-server logic
        # TODO tutaj musimy porozmawiać o komunikacji
        print("Game is starting")
        # some example opening of LobbyWindow
        self.__init_lobby_window()

    def __init_lobby_window(self):
        # TODO here opening LobbyWindow is a bit more complicated than in map_generator and requires info from server
        pass

    def on_click(self):
        host_address = self.text_line.text().strip()  # using strip() for annoying white chars surrounding address
        # TODO connect to client-server here
        try:
            socket.inet_aton(host_address)  # here put Błażej's code
            QMessageBox.question(self, "", "Successfully connected", QMessageBox.Ok, QMessageBox.Ok)
            # client-server's logic ...
            civ_combo = CivCombo(["zgredki", "elfy", "40-letnie-panny"],
                                 self)  # ["zgredki", "elfy", "40-letnie-panny"] should be civ_list returned from server

        except socket.error:
            QMessageBox.question(self, "host_address", "\"" + host_address + "\"" + " is incorrect address.",
                                 QMessageBox.Ok,
                                 QMessageBox.Ok)

    # typical function for getting window in the middle of a screen
    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
