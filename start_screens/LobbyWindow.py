from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QLineEdit, QPushButton, QMessageBox
import socket


class LobbyWindow(QMainWindow):
    def __init__(self):
        super(LobbyWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Game lobby")
        self.resize(100, 200)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
