from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget


# TODO add some info about unit being build back to CityView
class BuildUnitWindow(QMainWindow):
    """
    Going back to PyQt inside the game. Sadly that's the way it's gonna be.
    It was generated inside Qt Designer, so don't be surprised by the retranslateUi method.
    The main thing that this window does is calculating cost of building unit. You can mess with number of soldiers
    inside one group. Also, so far you are available to chose between Settler and 3 war units.
    """

    def __init__(self, parent, grandparent):
        super(BuildUnitWindow, self).__init__()
        self.unit_cost_holder = {"gold": 0, "wood": 0, "stone": 0, "food": 0, "time": 0}  # for one person unit
        self.total_cost_holder = {"gold": 0, "wood": 0, "stone": 0, "food": 0, "time": 0}  # for all unit
        self.unit_type_holder = None
        self.parent = parent  # for calling method inside parent object (BuildUnitFlatButton)
        self.grandparent = grandparent  # for calling method inside parent's parent object (CityView)

        self.resize(453, 480)
        self.centralwidget = QtWidgets.QWidget()

        self.how_many_slider = QtWidgets.QSlider(self.centralwidget)
        self.how_many_slider.setGeometry(QtCore.QRect(20, 210, 331, 20))
        self.how_many_slider.setOrientation(QtCore.Qt.Horizontal)
        self.how_many_slider.setMinimum(1)
        self.how_many_slider.setMaximum(100)
        self.how_many_slider.setTickInterval(10)  # works when you click next to slider
        self.how_many_slider.setSingleStep(10)
        self.how_many_slider.valueChanged.connect(self.recalculate_how_many)
        self.how_many_slider.setValue(1)

        self.how_many_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.how_many_line_edit.setGeometry(QtCore.QRect(360, 210, 81, 21))
        self.how_many_line_edit.setText("0")
        self.how_many_line_edit.textChanged.connect(self.change_slider_from_line_edit)  # both way changing value

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(40, 70, 151, 21))
        self.radioButton.toggled.connect(self.choose_unit)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 40, 141, 21))
        self.radioButton_2.toggled.connect(self.choose_unit)

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(40, 100, 141, 21))
        self.radioButton_3.toggled.connect(self.choose_unit)

        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(40, 130, 151, 21))
        self.radioButton_4.toggled.connect(self.choose_unit)

        self.build_button = QtWidgets.QPushButton(self.centralwidget)
        self.build_button.setGeometry(QtCore.QRect(148, 394, 141, 61))
        self.build_button.clicked.connect(self.build)

        self.not_enough_label = QtWidgets.QLabel(self.centralwidget)
        self.not_enough_label.setGeometry(QtCore.QRect(110, 360, 300, 21))
        self.not_enough_label.setText("You don't have enough resources.")
        self.not_enough_label.setStyleSheet("color: rgb(255, 77, 77);")
        self.not_enough_label.setVisible(False)

        self.no_unit_type_label = QtWidgets.QLabel(self.centralwidget)
        self.no_unit_type_label.setGeometry(QtCore.QRect(70, 360, 310, 21))
        self.no_unit_type_label.setText("Would you like to build some air? Choose unit.")
        self.no_unit_type_label.setStyleSheet("color: rgb(32,178,170);")
        self.no_unit_type_label.setVisible(False)

        self.how_many_label = QtWidgets.QLabel(self.centralwidget)
        self.how_many_label.setGeometry(QtCore.QRect(180, 180, 71, 21))

        self.cost_label = QtWidgets.QLabel(self.centralwidget)
        self.cost_label.setGeometry(QtCore.QRect(200, 250, 41, 21))

        self.gold_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.gold_line_edit.setGeometry(QtCore.QRect(60, 280, 41, 21))
        # self.gold_line_edit.setDisabled(True)

        self.gold_label = QtWidgets.QLabel(self.centralwidget)
        self.gold_label.setGeometry(QtCore.QRect(20, 280, 41, 21))

        self.wood_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.wood_line_edit.setGeometry(QtCore.QRect(170, 280, 41, 21))
        # self.wood_line_edit.setDisabled(True)

        self.wood_label = QtWidgets.QLabel(self.centralwidget)
        self.wood_label.setGeometry(QtCore.QRect(120, 280, 41, 21))

        self.stone_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.stone_line_edit.setGeometry(QtCore.QRect(270, 280, 41, 21))
        # self.stone_line_edit.setDisabled(True)

        self.stone_label = QtWidgets.QLabel(self.centralwidget)
        self.stone_label.setGeometry(QtCore.QRect(220, 280, 41, 21))

        self.food_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.food_line_edit.setGeometry(QtCore.QRect(360, 280, 41, 21))
        # self.food_line_edit.setDisabled(True)

        self.food_label = QtWidgets.QLabel(self.centralwidget)
        self.food_label.setGeometry(QtCore.QRect(320, 280, 41, 21))

        self.time_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.time_line_edit.setGeometry(QtCore.QRect(210, 310, 41, 21))
        # self.time_line_edit.setDisabled(True)

        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(170, 310, 41, 21))

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi(self)
        self.__center()

    def retranslateUi(self, MainWindow):
        """
        If someone would want to change units' names, it should be done here, and in chose_unit.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Build Unit"))
        self.radioButton.unit = "Poor Infantry"
        self.radioButton.setText(_translate("MainWindow", self.radioButton.unit))
        self.radioButton_2.unit = "Settler"
        self.radioButton_2.setText(_translate("MainWindow", self.radioButton_2.unit))
        self.radioButton_3.unit = "Archers"
        self.radioButton_3.setText(_translate("MainWindow", self.radioButton_3.unit))
        self.radioButton_4.unit = "Cavalry"
        self.radioButton_4.setText(_translate("MainWindow", self.radioButton_4.unit))
        self.how_many_label.setText(_translate("MainWindow", "How many"))
        self.cost_label.setText(_translate("MainWindow", "Cost:"))
        self.gold_label.setText(_translate("MainWindow", "gold"))
        self.wood_label.setText(_translate("MainWindow", "wood"))
        self.stone_label.setText(_translate("MainWindow", "stone"))
        self.food_label.setText(_translate("MainWindow", "food"))
        self.time_label.setText(_translate("MainWindow", "time"))
        self.build_button.setText(_translate("MainWindow", "Build"))

    def choose_unit(self):
        """
        Here values should be optimized.
        """
        radio_button = self.sender()
        if radio_button.isChecked():
            if radio_button.unit == self.radioButton_2.unit:  # Settler
                self.unit_cost_holder = {"gold": 20, "wood": 10, "stone": 0, "food": 100, "time": 1.0}
                self.how_many_line_edit.setText("1")
                self.how_many_line_edit.setDisabled(True)
                self.how_many_slider.setDisabled(True)
            else:
                self.how_many_line_edit.setDisabled(False)
                self.how_many_slider.setDisabled(False)

            if radio_button.unit == self.radioButton.unit:  # Infantry
                self.unit_cost_holder = {"gold": 3, "wood": 1, "stone": 0, "food": 10, "time": 0.05}

            if radio_button.unit == self.radioButton_3.unit:  # Archers
                self.unit_cost_holder = {"gold": 4, "wood": 3, "stone": 0, "food": 5, "time": 0.1}

            if radio_button.unit == self.radioButton_4.unit:  # Cavalry
                self.unit_cost_holder = {"gold": 7, "wood": 3, "stone": 2, "food": 20, "time": 0.3}

            self.unit_type_holder = radio_button.unit
            self.recalculate_costs()

    def recalculate_how_many(self):
        self.how_many_line_edit.setText(str(self.how_many_slider.value()))

    def recalculate_costs(self):
        """
        Calculates and sets value of total unit cost in total_cost_holder.
        It takes to consider building existing in this city.
        """
        how_many = int(self.how_many_line_edit.text())
        for key in self.unit_cost_holder:
            self.total_cost_holder[key] = int(self.unit_cost_holder[key] * how_many)

        if self.total_cost_holder["time"] == 0:
            self.total_cost_holder["time"] = 1  # making a unit always costs at least a day

        if self.grandparent.city.buildings["Armory"]:
            self.total_cost_holder["wood"] = int(self.total_cost_holder["wood"] * 0.85)
            self.total_cost_holder["stone"] = int(self.total_cost_holder["stone"] * 0.85)

        if self.grandparent.city.buildings["Passiflora"]:
            self.total_cost_holder["gold"] = int(self.total_cost_holder["gold"] * 0.8)
            self.total_cost_holder["food"] = int(self.total_cost_holder["food"] * 0.8)

        self.gold_line_edit.setText(str(self.total_cost_holder["gold"]))
        self.wood_line_edit.setText(str(self.total_cost_holder["wood"]))
        self.stone_line_edit.setText(str(self.total_cost_holder["stone"]))
        self.food_line_edit.setText(str(self.total_cost_holder["food"]))
        self.time_line_edit.setText(str(self.total_cost_holder["time"]))

        self.not_enough_label.setVisible(False)
        self.no_unit_type_label.setVisible(False)

    def change_slider_from_line_edit(self):
        try:
            number = int(self.how_many_line_edit.text())
            if number < 1:
                number = 1
                self.how_many_line_edit.setText(str(number))
            elif number > 100:
                number = 100
                self.how_many_line_edit.setText(str(number))
        except:  # catches all strange input
            number = 1
            self.how_many_line_edit.setText(str(number))
        self.how_many_slider.setValue(number)
        self.recalculate_costs()

    def build(self):
        """
        If player has enough materials building unit starts else player gets prompt.
        This method exits this window by calling kill_app in BuildUnitFlatButton object.
        Also saves calculated total value inside CityView object.
        """
        if not self.grandparent.city.owner.granary.is_enough(self.total_cost_holder):
            self.no_unit_type_label.setVisible(False)
            self.not_enough_label.setVisible(True)
        elif self.unit_type_holder is None:
            self.not_enough_label.setVisible(False)
            self.no_unit_type_label.setVisible(True)
        else: # this happens when everything is ok and unit building starts
            self.grandparent.city.owner.granary.pay_for(self.total_cost_holder) # paying for unit

            self.grandparent.transport_unit_building_costs(self.total_cost_holder)
            count = self.how_many_slider.value()
            print(f"Requested unit {self.unit_type_holder}")
            self.grandparent.city.unit_request = {'type': self.unit_type_holder, 'count': count}
            self.grandparent.city.days_left_to_building_completion = self.total_cost_holder["time"]

            self.grandparent.city.building_request = None
            self.hide()
            self.parent.kill_app()

    def closeEvent(self, event) -> None:
        self.parent.kill_app()

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# for testing
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuildUnitWindow(None, None)
    win.show()
    sys.exit(app.exec_())
