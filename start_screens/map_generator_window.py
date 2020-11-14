import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QPushButton, \
    QLineEdit, QLabel


class MapGeneratorWindow(QMainWindow):
    def __init__(self):
        super(MapGeneratorWindow, self).__init__()
        self.map = None
        self.generate_button = None
        self.ok_button = None
        self.seed_line = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Age of Divisiveness - Map Generator")
        self.setFixedSize(800, 600)

        self.map = QLabel(self)
        self.map.setGeometry(QRect(6, 10, 781, 521))
        pixmap = QPixmap('images/example_map.jpg')
        self.map.setPixmap(pixmap)
        self.map.setScaledContents(True)

        self.seed_line = QLineEdit(self)
        self.seed_line.setText("Enter seed.")
        self.seed_line.setGeometry(QRect(10, 550, 370, 41))

        self.generate_button = QPushButton(self)
        self.generate_button.setText("Generate")
        self.generate_button.setGeometry(QRect(390, 550, 190, 41))
        self.generate_button.clicked.connect(self.generate_map)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setGeometry(QRect(590, 550, 191, 41))
        self.ok_button.clicked.connect(self.start_game)

        self.center()
        self.show()

    def generate_map(self):
        # TODO this function should use MapGenerator interface and set new pixmap. self.map will refresh automatically.
        seed = self.seed_line.text()  # this way you get seed_line value
        print(seed)
        new_map = QPixmap('images/example_map_2.png')
        self.map.setPixmap(new_map)

    def start_game(self):
        # TODO
        print("Game is starting")

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
