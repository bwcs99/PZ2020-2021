import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget


class BuildBuildingWindow(QMainWindow):
    """
    The most important window when it comes to experience of building civilization.
    To be added - inside view of Passiflora.
    """

    def __init__(self, parent, grandparent):
        super(BuildBuildingWindow, self).__init__()
        self.building_cost_holder = {"gold": 0, "wood": 0, "stone": 0, "food": 0, "time": 0}
        self.building_type_holder = None

        self.setWindowTitle("Buildings")
        self.resize(450, 660)
        self.parent = parent  # for calling method inside parent object (BuildUnitFlatButton)
        self.grandparent = grandparent  # for calling method inside parent's parent object (CityView)

        self.centralwidget = QtWidgets.QWidget()

        """ BUILDINGS PART """

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 30, 211, 16))
        self.label.setText("Astronomic Tower")

        self.label_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_desc.setGeometry(QtCore.QRect(120, 50, 211, 40))
        self.label_desc.setWordWrap(True)
        self.label_desc.setStyleSheet("color: rgb(150, 150, 81)")
        self.label_desc.setText("Allows city borders to grow.")

        self.image_1 = QtWidgets.QLabel(self.centralwidget)
        self.image_1.setGeometry(QtCore.QRect(20, 20, 81, 71))
        pixmap = QPixmap(os.getcwd() + '/resources/images/buildings/astronomic_tower.png')
        self.image_1.setPixmap(pixmap)
        self.image_1.setScaledContents(True)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 120, 211, 16))
        self.label_2.setText("Mines")

        self.label_2_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_2_desc.setGeometry(QtCore.QRect(120, 140, 211, 40))
        self.label_2_desc.setWordWrap(True)
        self.label_2_desc.setStyleSheet("color: rgb(150, 150, 81)")
        self.label_2_desc.setText("Produces extra 20 stone per turn.")

        self.image_2 = QtWidgets.QLabel(self.centralwidget)
        self.image_2.setGeometry(QtCore.QRect(20, 110, 81, 71))
        pixmap = QPixmap(os.getcwd() + '/resources/images/buildings/mines.png')
        self.image_2.setPixmap(pixmap)
        self.image_2.setScaledContents(True)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(120, 210, 211, 16))
        self.label_9.setText("Free Market")

        self.label_9_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_9_desc.setGeometry(QtCore.QRect(120, 230, 211, 40))
        self.label_9_desc.setWordWrap(True)
        self.label_9_desc.setStyleSheet("color: rgb(150, 150, 81)")
        self.label_9_desc.setText("Every city area square brings extra 3 gold.")

        self.image_3 = QtWidgets.QLabel(self.centralwidget)
        self.image_3.setGeometry(QtCore.QRect(20, 200, 81, 71))
        pixmap = QPixmap(os.getcwd() + '/resources/images/buildings/free_market.png')
        self.image_3.setPixmap(pixmap)
        self.image_3.setScaledContents(True)

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(120, 300, 211, 16))
        self.label_10.setText("Armory")

        self.label_10_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_10_desc.setGeometry(QtCore.QRect(120, 320, 211, 40))
        self.label_10_desc.setWordWrap(True)
        self.label_10_desc.setStyleSheet("color: rgb(150, 150, 81)")
        self.label_10_desc.setText("All units cost 15% less wood and stone.")

        self.image_4 = QtWidgets.QLabel(self.centralwidget)
        self.image_4.setGeometry(QtCore.QRect(20, 290, 81, 71))
        pixmap = QPixmap(os.getcwd() + '/resources/images/buildings/armory.png')
        self.image_4.setPixmap(pixmap)
        self.image_4.setScaledContents(True)

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(120, 390, 211, 16))
        self.label_11.setText("Passiflora")

        self.label_11_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_11_desc.setGeometry(QtCore.QRect(120, 410, 211, 40))
        self.label_11_desc.setWordWrap(True)
        self.label_11_desc.setStyleSheet("color: rgb(150, 150, 81)")
        self.label_11_desc.setText("All units cost 20% less food and gold.")

        self.image_5 = QtWidgets.QLabel(self)
        self.image_5.setGeometry(QtCore.QRect(20, 380, 81, 71))
        pixmap = QPixmap(os.getcwd() + '/resources/images/buildings/passiflora.png')
        self.image_5.setPixmap(pixmap)
        self.image_5.setScaledContents(True)

        """ COSTS PART """

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(322, 506, 41, 21))
        self.label_6.setText("food")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(122, 506, 41, 21))
        self.label_4.setText("wood")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(22, 506, 41, 21))
        self.label_3.setText("gold")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(172, 536, 41, 21))
        self.label_7.setText("time")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(202, 476, 41, 21))
        self.label_5.setText("Cost:")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(222, 506, 41, 21))
        self.label_8.setText("stone")

        self.gold_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.gold_line_edit.setGeometry(QtCore.QRect(62, 506, 41, 21))

        self.wood_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.wood_line_edit.setGeometry(QtCore.QRect(172, 506, 41, 21))

        self.stone_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.stone_line_edit.setGeometry(QtCore.QRect(272, 506, 41, 21))

        self.food_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.food_line_edit.setGeometry(QtCore.QRect(362, 506, 41, 21))

        self.time_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.time_line_edit.setGeometry(QtCore.QRect(212, 536, 41, 21))

        """ RADIO BUTTONS PART"""

        self.build_button = QtWidgets.QPushButton(self.centralwidget)
        self.build_button.setGeometry(QtCore.QRect(150, 570, 141, 61))
        self.build_button.setText("Build")
        self.build_button.clicked.connect(self.build)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(350, 50, 21, 21))
        self.radioButton.setText("")
        self.radioButton.building = "Astronomic Tower"
        self.radioButton.toggled.connect(self.choose_building)
        if self.grandparent.city.buildings["Astronomic Tower"]: self.radioButton.setVisible(False)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(350, 140, 21, 21))
        self.radioButton_2.setText("")
        self.radioButton_2.building = "Mines"
        self.radioButton_2.toggled.connect(self.choose_building)
        if self.grandparent.city.buildings["Mines"]: self.radioButton_2.setVisible(False)

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(350, 230, 21, 21))
        self.radioButton_3.setText("")
        self.radioButton_3.building = "Free Market"
        self.radioButton_3.toggled.connect(self.choose_building)
        if self.grandparent.city.buildings["Free Market"]: self.radioButton_3.setVisible(False)

        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(350, 320, 21, 21))
        self.radioButton_4.setText("")
        self.radioButton_4.building = "Armory"
        self.radioButton_4.toggled.connect(self.choose_building)
        if self.grandparent.city.buildings["Armory"]: self.radioButton_4.setVisible(False)

        self.radioButton_5 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_5.setGeometry(QtCore.QRect(350, 410, 21, 21))
        self.radioButton_5.setText("")
        self.radioButton_5.building = "Passiflora"
        self.radioButton_5.toggled.connect(self.choose_building)
        if self.grandparent.city.buildings["Passiflora"]: self.radioButton_5.setVisible(False)

        """ INVISIBLE LABELS """

        self.not_enough_label = QtWidgets.QLabel(self.centralwidget)
        self.not_enough_label.setGeometry(QtCore.QRect(110, 455, 300, 21))
        self.not_enough_label.setText("You don't have enough resources.")
        self.not_enough_label.setStyleSheet("color: rgb(255, 77, 77);")
        self.not_enough_label.setVisible(False)

        self.no_building_type_label = QtWidgets.QLabel(self.centralwidget)
        self.no_building_type_label.setGeometry(QtCore.QRect(30, 455, 400, 21))
        self.no_building_type_label.setText(
            "Here is stubble for now, but there will be San Francisco.")
        self.no_building_type_label.setStyleSheet("color: rgb(32,178,170);")
        self.no_building_type_label.setVisible(False)

        self.setCentralWidget(self.centralwidget)

    def choose_building(self):
        """
        Here costs should be optimized.
        """
        radio_button = self.sender()
        if radio_button.isChecked():

            if radio_button.building == self.radioButton.building:  # Astronomic Tower
                self.building_cost_holder = {"gold": 150, "wood": 300, "stone": 50, "food": 10, "time": 4}

            if radio_button.building == self.radioButton_2.building:  # Mines
                self.building_cost_holder = {"gold": 150, "wood": 400, "stone": 0, "food": 230, "time": 5}

            if radio_button.building == self.radioButton_3.building:  # Free Market
                self.building_cost_holder = {"gold": 300, "wood": 320, "stone": 70, "food": 320, "time": 4}

            if radio_button.building == self.radioButton_4.building:  # Armory
                self.building_cost_holder = {"gold": 260, "wood": 300, "stone": 110, "food": 120, "time": 6}

            if radio_button.building == self.radioButton_5.building:  # Passiflora
                self.building_cost_holder = {"gold": 310, "wood": 400, "stone": 200, "food": 400, "time": 4}

            self.building_type_holder = radio_button.building
            self.set_costs()

    def set_costs(self):
        """
        Sets building cost in appropriate line edits fields.
        """

        self.gold_line_edit.setText(str(self.building_cost_holder["gold"]))
        self.wood_line_edit.setText(str(self.building_cost_holder["wood"]))
        self.stone_line_edit.setText(str(self.building_cost_holder["stone"]))
        self.food_line_edit.setText(str(self.building_cost_holder["food"]))
        self.time_line_edit.setText(str(self.building_cost_holder["time"]))

        self.not_enough_label.setVisible(False)
        self.no_building_type_label.setVisible(False)

    def build(self):
        """
        If player has enough materials building building starts else player gets prompt.
        This method exits this window by calling kill_app in BuildBuildingFlatButton object.
        Also saves calculated total value inside CityView object.
        """

        if not self.grandparent.city.owner.granary.is_enough(self.building_cost_holder):
            self.no_building_type_label.setVisible(False)
            self.not_enough_label.setVisible(True)
        elif self.building_type_holder is None:
            self.not_enough_label.setVisible(False)
            self.no_building_type_label.setVisible(True)
        else:
            self.grandparent.city.owner.granary.pay_for(self.building_cost_holder)  # paying for building

            self.grandparent.transport_building_building_costs(self.building_cost_holder)
            self.grandparent.city.days_left_to_building_building_completion = self.building_cost_holder["time"]
            self.grandparent.city.building_request = self.building_type_holder

            self.grandparent.city.unit_request = None

            self.hide()
            self.parent.kill_app()

    def closeEvent(self, event) -> None:
        self.parent.kill_app()

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuildBuildingWindow(None, None)
    win.show()
    sys.exit(app.exec_())
