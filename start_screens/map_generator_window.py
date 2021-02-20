import os
import sys
import threading

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QPushButton, \
    QLineEdit, QLabel, QToolTip

from map_generation import generate_map
from server_utils.server import Server
from start_screens import img_gen
from start_screens.lobby_window import LobbyWindow
from start_screens.nick_civ_window import CivCombo


class MapGeneratorWindow(QMainWindow):
    """
    This Window is responsible for two things:
    1. connecting map_generator interface to gui and allowing user to generate maps based on seed,
    2. creating thread for server, server afterwards is kept parallel to the rest of application.
    """

    def __init__(self, parent):
        super(MapGeneratorWindow, self).__init__()
        self.parent = parent
        self.world_map_matrix = None
        self.chosen_civ = "fat_dwarves"
        self.chosen_nick = "fat_Bob"
        self.server = None
        self.server_thread = None
        self.server_ready = threading.Event()

        self.setWindowTitle("Age of Divisiveness - Map Generator")
        self.setFixedSize(1000, 540)

        self.map = QLabel(self)
        self.map.setGeometry(QRect(10, 10, 781, 521))
        self.map.setScaledContents(True)

        self.height_label = QLabel(self)
        self.height_label.setGeometry(QRect(870, 20, 60, 30))
        self.height_label.setText("Height")
        self.height_edit = QLineEdit(self)
        self.height_edit.setGeometry(QRect(865, 50, 60, 30))
        self.height_edit.setText("50")

        self.width_label = QLabel(self)
        self.width_label.setGeometry(QRect(870, 80, 60, 30))
        self.width_label.setText("Width")
        self.width_edit = QLineEdit(self)
        self.width_edit.setGeometry(QRect(865, 110, 60, 30))
        self.width_edit.setText("80")

        self.seed_label = QLabel(self)
        self.seed_label.setGeometry(QRect(875, 140, 120, 30))
        self.seed_label.setText("Seed")
        self.seed_edit = QLineEdit(self)
        self.seed_edit.setGeometry(QRect(865, 170, 60, 30))
        self.seed_edit.setText("3")

        self.plains_label = QLabel(self)
        self.plains_label.setGeometry(QRect(870, 200, 60, 30))
        self.plains_label.setText("Plains")
        self.plains_edit = QLineEdit(self)
        self.plains_edit.setGeometry(QRect(865, 230, 60, 30))
        self.plains_edit.setText("4")

        self.hills_label = QLabel(self)
        self.hills_label.setGeometry(QRect(875, 260, 60, 30))
        self.hills_label.setText("Hills")
        self.hills_edit = QLineEdit(self)
        self.hills_edit.setGeometry(QRect(865, 290, 60, 30))
        self.hills_edit.setText("11")

        self.mountains_label = QLabel(self)
        self.mountains_label.setGeometry(QRect(860, 320, 100, 30))
        self.mountains_label.setText("Mountains")
        self.mountains_edit = QLineEdit(self)
        self.mountains_edit.setGeometry(QRect(865, 350, 60, 30))
        self.mountains_edit.setText("20")

        QToolTip.setFont(QFont('SansSerif', 14))

        self.question_mark = QLabel(self)
        self.question_mark.setPixmap(QPixmap(os.getcwd() + '/resources/images/question_mark.png'))
        self.question_mark.setGeometry(QRect(950, 350, 25, 25))
        self.question_mark.setScaledContents(True)
        self.question_mark.setToolTip("<b>Width</b> - number of tiles in width <br>"
                                      "<b>Height</b> - number of tiles in height <br>"
                                      "Recommended ratio is 5:8 <br><br>"
                                      "<b>Seed</b> - is used to generate different maps from the same parameters <br><br>"
                                      "Next parameters determine level on which chosen tile type stop to appear. You can imagine it ass flood, so tiles with given altitude won't be covered by water, but those with smaller altitude will be.<br>"
                                      "It's important to notice that hills should have higher altitude than plains and mountains should have higher than hills. Otherwise obscure maps will be generated and some materials may not be present. <br>"
                                      "But fell free to experiment.")

        self.generate_button = QPushButton(self)
        self.generate_button.setText("Generate")
        self.generate_button.setGeometry(QRect(800, 390, 190, 41))
        self.generate_button.clicked.connect(self.generate_map)

        self.ok_button = QPushButton(self)
        self.ok_button.setText("OK")
        self.ok_button.setGeometry(QRect(800, 440, 190, 41))
        self.ok_button.clicked.connect(self.prepare_for_game)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.setGeometry(QRect(800, 490, 190, 41))
        self.back_button.clicked.connect(self.__go_back)

        self.center()
        self.show()
        self.generate_map()  # generate default map

    def generate_map(self):
        """
        Generate world map and show its overview using 6 parameters from textfields in following order:
        Look 'generate_map' for more info.
        """
        try:
            h = int(self.height_edit.text())
            w = int(self.width_edit.text())
            sd = int(self.seed_edit.text())
            p1 = int(self.plains_edit.text())
            p2 = int(self.hills_edit.text())
            p3 = int(self.mountains_edit.text())
        except ValueError:
            return

        self.world_map_matrix = generate_map(height=h, width=w, params=[sd, p1, p2, p3])  # get world matrix
        image = img_gen.get_map_overview(self.world_map_matrix)  # get image overview of generated world
        image = img_gen.get_resized_map_overview(image, 781, 521)
        qim = ImageQt(image).copy()
        new_map = QPixmap.fromImage(qim)  # convert to QPixmap
        self.map.setPixmap(new_map)  # display

    def prepare_for_game(self):
        """
        When CivCombo object is created, window opens, and after closing it changes self.chosen_civ field in
        parent object by calling set_player_info method from CivCombo.
        """

        CivCombo(["The Great Northern", "Kaediredameria", "Mixtec", "Kintsugi"],
                 self)  # here should be all civilizations

    def set_player_info(self, chosen_civ, chosen_nick):
        """ This method ic called within CivCombo. DON'T CHANGE this function's name, even with refactor. """
        self.chosen_civ = chosen_civ
        self.chosen_nick = chosen_nick

        # print(self.chosen_civ, self.chosen_nick)
        self.start_server()

    def create_server_thread(self):
        """
        This is thread method. This method transpose game matrix, cause then it's easier to use in game_screens.
        Also creates server object which is now listening for connections.
        """
        self.world_map_matrix = [
            [self.world_map_matrix[y][x] for y in range(len(self.world_map_matrix))]
            for x in range(len(self.world_map_matrix[0]))
        ]
        self.server = Server(self.world_map_matrix)
        self.server_ready.set()
        self.server.start_connection()

    def start_server(self):
        """ Starting thread with server """
        print("Server is starting...")
        self.server_thread = threading.Thread(target=self.create_server_thread, args=())
        self.server_thread.start()
        self.__init_lobby_window()  # this line continues flow of main thread to lobby window.

    def __init_lobby_window(self):
        self.server_ready.wait()  # time for server to setup
        self.lobby_window = LobbyWindow(True, self.chosen_nick, self.chosen_civ,
                                        server_object=self.server)  # True because this is host.
        self.lobby_window.server_thread = self.server_thread
        self.lobby_window.show()
        self.hide()

    def __go_back(self):
        self.close()
        self.parent.show()

    def center(self):  # center window on screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# for testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MapGeneratorWindow(None)
    win.show()
    sys.exit(app.exec_())
