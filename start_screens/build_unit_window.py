from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class BuildUnitWindow(QMainWindow):
    def __init__(self, parent):
        super(BuildUnitWindow, self).__init__()
        self.unit_cost_holder = dict()
        self.parent = parent

        self.resize(453, 415)
        self.centralwidget = QtWidgets.QWidget()

        self.how_many_slider = QtWidgets.QSlider(self.centralwidget)
        self.how_many_slider.setGeometry(QtCore.QRect(20, 210, 331, 20))
        self.how_many_slider.setOrientation(QtCore.Qt.Horizontal)
        self.how_many_slider.setMinimum(0)
        self.how_many_slider.setMaximum(100)
        self.how_many_slider.setTickInterval(10)
        self.how_many_slider.setSingleStep(10)

        self.how_many_slider.valueChanged.connect(self.recalculate_costs)

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(40, 70, 151, 21))
        self.radioButton.toggled.connect(self.chose_unit)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 40, 141, 21))
        self.radioButton_2.toggled.connect(self.chose_unit)

        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(40, 100, 141, 21))
        self.radioButton_3.toggled.connect(self.chose_unit)

        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(40, 130, 151, 21))
        self.radioButton_4.toggled.connect(self.chose_unit)

        self.build_button = QtWidgets.QPushButton(self.centralwidget)
        self.build_button.setGeometry(QtCore.QRect(148, 344, 141, 61))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 180, 71, 21))

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 250, 41, 21))

        self.how_many_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.how_many_line_edit.setGeometry(QtCore.QRect(360, 210, 81, 21))
        self.how_many_line_edit.setText("0")
        self.how_many_line_edit.textChanged.connect(self.change_slider_from_line_edit)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 280, 41, 21))

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 280, 41, 21))

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(170, 280, 41, 21))

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 280, 41, 21))

        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(270, 280, 41, 21))

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(220, 280, 41, 21))

        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(360, 280, 41, 21))

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(320, 280, 41, 21))

        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(210, 310, 41, 21))

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(170, 310, 41, 21))

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton.setText(_translate("MainWindow", "Biedne Piechota"))
        self.radioButton.unit = "Biedne Piechota"
        self.radioButton_2.setText(_translate("MainWindow", "Settler"))
        self.radioButton_2.unit = "Settler"
        self.radioButton_3.setText(_translate("MainWindow", "Łucznicy"))
        self.radioButton_3.unit = "Łucznicy"
        self.radioButton_4.setText(_translate("MainWindow", "Cięzka Kawaleria"))
        self.radioButton_4.unit = "Cięzka Kawaleria"
        self.label.setText(_translate("MainWindow", "How many"))
        self.label_2.setText(_translate("MainWindow", "Cost:"))
        self.label_3.setText(_translate("MainWindow", "gold"))
        self.label_4.setText(_translate("MainWindow", "wood"))
        self.label_5.setText(_translate("MainWindow", "stone"))
        self.label_6.setText(_translate("MainWindow", "food"))
        self.label_7.setText(_translate("MainWindow", "time"))
        self.build_button.setText(_translate("MainWindow", "Build"))

    def chose_unit(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            if radio_button.unit == "Settler":
                self.unit_cost_holder = {"gold": 20, "wood": 10, "stone": 0, "food": 100, "time": 1.0}

    def recalculate_costs(self):
        self.how_many_line_edit.setText(str(self.how_many_slider.value()))

    def change_slider_from_line_edit(self):
        try:
            number = int(self.how_many_line_edit.text())
            if number < 0:
                number = 0
                self.how_many_line_edit.setText(str(number))
            elif number > 100:
                number = 100
                self.how_many_line_edit.setText(str(number))
        except:
            number = 0
            self.how_many_line_edit.setText(str(number))
        self.how_many_slider.setValue(number)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuildUnitWindow(None)
    win.show()
    sys.exit(app.exec_())
