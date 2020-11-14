from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, \
    QHBoxLayout, QComboBox
import socket
from PyQt5 import QtCore
from PyQt5.uic.uiparser import QtCore

from LobbyWindow import LobbyWindow

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age of Divisiveness"


class ConnectWindow(QMainWindow):

    def __init__(self):
        super(ConnectWindow, self).__init__()
        self.image_label = None
        self.text_line = None
        self.button = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Connect Window")

        # setting pixel art image as background
        self.image_label = QLabel(self)  # background label
        pixmap = QPixmap('images/novigrad.png')
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.setCentralWidget(self.image_label)
        self.resize(int(pixmap.width() * 1.5), int(pixmap.height() * 1.5))

        # creating text label in the window
        # if someone would like to try to remove content of self.text_line after
        # clicking on it I strongly recommend taking some painkillers and alcohol before
        self.text_line = QLineEdit(self)
        self.text_line.setText("127.0.0.1")
        self.text_line.move(20, 20)
        self.text_line.resize(280, 40)

        # creating button in the window
        self.button = QPushButton('Connect', self)
        self.button.move(20, 80)

        # connecting button to function on_click
        self.button.clicked.connect(self.on_click)

        self.center()
        self.show()

    # typical function for getting window in the middle of a screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def choose_civ(self):
        civ_combo = CivCombo(["elfy", "zgredki", "czarodzieje"], self)
        civ_combo.show()

        return 1

    def on_click(self):
        # using strip() in case of any annoying white chars surrounding address
        host_address = self.text_line.text().strip()
        # TODO connect to client-server here
        try:
            socket.inet_aton(host_address)  # kod Błażeja
            QMessageBox.question(self, "", "Successfully connected", QMessageBox.Ok, QMessageBox.Ok)
            civilization_id = self.choose_civ()

        except socket.error:
            QMessageBox.question(self, "host_address", "\"" + host_address + "\"" + " is incorrect address.",
                                 QMessageBox.Ok,
                                 QMessageBox.Ok)


class CivCombo(QMainWindow):
    def __init__(self, civ_list, parent=None):
        super(CivCombo, self).__init__(parent)
        self.setWindowTitle("Choose your civilization")
        self.setFixedSize(560, 140)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(civ_list)
        self.combo_box.setGeometry(QRect(10, 40, 421, 61))

        self.ok_button = QPushButton(self)
        self.ok_button.setText("Choose")
        self.ok_button.setGeometry(QRect(450, 40, 101, 61))
        self.ok_button.clicked.connect(self.init_lobby_window)

        self.center()

    def init_lobby_window(self):
        civilization = self.combo_box.currentText()  # this how you get value from combo box
        print(civilization)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
