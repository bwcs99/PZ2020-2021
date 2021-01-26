import sys
import webbrowser

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QLabel, QApplication, QVBoxLayout, QWidget, QPushButton, )


class AboutWindow(QMainWindow):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("About")
        self.setFixedSize(550, 700)
        layout = QVBoxLayout()
        about_text = QLabel(
            "<b>DESCRIPTION</b> <br>"
            "In a time of great conflict, new kingdoms are born in minds of ambitious rules and willing hearts of dedicated serfs. "
            "Every great kingdom needs a powerful army, vivid homeland culture and thoughtful diplomacy. "
            "Be ready to conquer civilizations and win extensive battles, in which the key to defeating your enemy will be both hands and minds. "
            "Will you win by being a despotic tyrant or maybe by creating a web of secret pacts? Will your kingdom story be written by romantic tales or fearful half lies? "
            "Nevertheless, keep your kingdom in order and do not find your domain in the age of divisiveness.",
            self)
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignCenter)
        about_text.move(10, 20)

        link_button = QPushButton()
        link_button.setMaximumHeight(150)
        link_button.setIconSize(QSize(300, 400))
        link_button.setIcon(QIcon("resources/images/aod_logo.png"))
        link_button.setFlat(True)
        link_button.clicked.connect(self.show_github)

        authors_text = QLabel(
            "<b>AUTHORS </b> <br> Patryk Majewski, Krzysztof Szymaniak, Gabriel Wechta, Błażej Wróbel")
        authors_text.setAlignment(Qt.AlignCenter)
        attributions_fonts = QLabel()
        attributions_fonts.setText(
            "<b>ATTRIBUTIONS</b> <br> <a href='https://www.1001fonts.com/november-font.html'>November</a> - in game font<br> <a href='https://fontenddev.com/fonts/alkhemikal/ '>Alkhemikal</a> - logo font")
        attributions_fonts.setOpenExternalLinks(True)
        attributions_fonts.setAlignment(Qt.AlignCenter)

        attributions_images = QLabel()
        attributions_images.setText("Image authors: <br> "
                                    "Aneta Pawska [<a href='https://commons.wikimedia.org/wiki/File:Ko%C5%9Bci%C3%B3%C5%82_Wang,_Karpacz.jpg#/media/File:Ko%C5%9Bci%C3%B3%C5%82_Wang,_Karpacz.jpg'>1</a>] <br>"
                                    "Paul Berzinn [<a href='https://commons.wikimedia.org/wiki/Category:Longhouse_at_Lofotr_Vikingmuseum#/media/File:Viking_museum_at_Borge_-_panoramio.jpg'>1</a>] <br>"
                                    "Jarek Tarnogórski [<a href='https://commons.wikimedia.org/wiki/Category:Archeopark_in_Chot%C4%9Bbuz#/media/File:Cieszynisko_017.JPG'>1</a>] <br>"
                                    "Boryslav Javir [<a href='https://commons.wikimedia.org/wiki/Category:Perun#/media/File:Perun7516_1_21.jpg'>1</a>] <br>"
                                    "Maunus [<a href='https://commons.wikimedia.org/wiki/File:StaCeciliaAcatitlanNorte.jpg'>1</a>] <br>"
                                    "Arian Zwegers [<a href='https://commons.wikimedia.org/wiki/File:El_Tajin,_Pyramid_of_the_Niches_(20686703945).jpg'>1</a>] "
                                    "[<a href='https://commons.wikimedia.org/wiki/File:Mitla,_Group_of_the_Columns,_Palace_of_Columns_(20064199284).jpg'>2</a>] <br>"
                                    "Martin Falbisoner [<a href='https://commons.wikimedia.org/wiki/File:Himeji_Castle,_November_2016_-02.jpg'>1</a>] <br>"
                                    "Basile Morin [<a href='https://commons.wikimedia.org/w/index.php?search=japan+&title=Special%3ASearch&go=Go&ns0=1&ns6=1&ns12=1&ns14=1&ns100=1&ns106=1#/media/File:Yasaka-dori_early_morning_with_street_lanterns_and_the_Tower_of_Yasaka_(Hokan-ji_Temple),_Kyoto,_Japan.jpg'>1</a>] <br>"
                                    "Nobrinskii [<a href='https://commons.wikimedia.org/wiki/File:Eigen-ji_(Rinzai_temple)_-_front_area.jpg'>1</a>] <br>")
        attributions_images.setOpenExternalLinks(True)
        attributions_images.setAlignment(Qt.AlignCenter)

        # for future development - "Aneta Pawska [<a href=''>1</a>] <br>"

        thanks_label = QLabel("Big thanks to all sources!")
        thanks_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(link_button)
        layout.addWidget(about_text)
        layout.addWidget(authors_text)
        layout.addWidget(attributions_fonts)
        layout.addWidget(attributions_images)
        layout.addWidget(thanks_label)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        main_widget.adjustSize()

        self.setCentralWidget(main_widget)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_github(self):
        webbrowser.open("https://github.com/bwcs99/PZ2020-2021")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AboutWindow()
    win.show()
    sys.exit(app.exec_())
