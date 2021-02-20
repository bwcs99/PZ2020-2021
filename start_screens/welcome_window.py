import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QDesktopWidget, \
    QVBoxLayout, QPushButton

from start_screens.about_window import AboutWindow
from start_screens.connect_window import ConnectWindow
from start_screens.map_generator_window import MapGeneratorWindow


class WelcomeWindow(QMainWindow):
    """
    This is main window of the application.
    From here we can go to ConnectWindow and LobbyWindow
    class has two fields responsible for holding newly created windows.
    """

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.connect_window = None
        self.map_generator_window = None
        self.about_window = None
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Age of Divisiveness")
        self.__put_buttons()
        self.setFixedSize(480, 400)
        self.__center()
        self.show()

    def __put_buttons(self):
        up_wid = QWidget(self)
        down_wid = QWidget(self)
        up_layout = QVBoxLayout()
        down_layout = QVBoxLayout()
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()

        connect_button = QPushButton('Connect to server', self)
        connect_button.clicked.connect(self.__init_connect_to_server_window)
        down_layout.addWidget(connect_button)

        host_button = QPushButton('Host your game', self)
        host_button.clicked.connect(self.__init_map_generator_window)
        down_layout.addWidget(host_button)

        about_button = QPushButton('Read about', self)
        about_button.clicked.connect(self.__show_about)
        down_layout.addWidget(about_button)

        image_label = QLabel(self)  # background image label
        pixmap = QPixmap('resources/images/aod_logo.png')  # path to logo.png
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)

        up_wid.setLayout(up_layout)
        down_wid.setLayout(down_layout)
        main_layout.addWidget(up_wid)
        main_layout.addWidget(image_label)
        main_layout.addWidget(down_wid)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init_connect_to_server_window(self):
        self.connect_window = ConnectWindow(self)
        self.connect_window.show()
        self.close()

    def __init_map_generator_window(self):
        self.map_generator_window = MapGeneratorWindow(self)
        self.map_generator_window.show()
        self.close()

    def __show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()



# for testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WelcomeWindow()
    win.show()
    sys.exit(app.exec_())
