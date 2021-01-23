from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class BuyGoodsWindow(QMainWindow):
    """

    """

    def __init__(self, parent, grandparent):
        super(BuyGoodsWindow, self).__init__()
        self.resize(630, 320)
        self.setWindowTitle(" ")  # TODO
        self.gold_dict = {"gold": 0, "wood": 0, "stone": 0,
                          "food": 0}  # this dictionary is only used for holding keep of gold, but it's used couple of times so it will be easier to declare it.

        self.centralwidget = QtWidgets.QWidget()

        """ RADIO BUTTONS PART """

        self.wood_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.wood_radio_button.setGeometry(QtCore.QRect(60, 50, 112, 23))
        self.wood_radio_button.setText("Wood")
        self.wood_radio_button.material = "Wood"
        self.wood_radio_button.clicked.connect(self.make_offer)

        self.stone_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.stone_radio_button.setGeometry(QtCore.QRect(60, 100, 112, 23))
        self.stone_radio_button.setText("Stone")
        self.stone_radio_button.material = "Stone"
        self.stone_radio_button.clicked.connect(self.make_offer)

        self.food_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.food_radio_button.setGeometry(QtCore.QRect(60, 150, 112, 23))
        self.food_radio_button.setText("Food")
        self.food_radio_button.material = "Food"
        self.food_radio_button.clicked.connect(self.make_offer)

        """ HOW MANY PART """

        self.how_many_slider = QtWidgets.QSlider(self.centralwidget)
        self.how_many_slider.setGeometry(QtCore.QRect(240, 80, 241, 16))
        self.how_many_slider.setOrientation(QtCore.Qt.Horizontal)
        self.how_many_slider.setMinimum(1)
        self.how_many_slider.setMaximum(500)
        self.how_many_slider.setTickInterval(10)  # works when you click next to slider
        self.how_many_slider.setSingleStep(10)
        self.how_many_slider.valueChanged.connect(self.recalculate_how_many)
        self.how_many_slider.setValue(1)

        self.how_many_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.how_many_edit.setGeometry(QtCore.QRect(500, 70, 113, 25))
        self.how_many_edit.setText("1")
        self.how_many_edit.textChanged.connect(self.change_slider_from_line_edit)  # both way changing value

        self.how_many_label = QtWidgets.QLabel(self.centralwidget)
        self.how_many_label.setGeometry(QtCore.QRect(290, 30, 241, 17))
        self.how_many_label.setText("How many would you like to buy?")

        """ HOW MUCH PART """

        self.how_much_for_piece_label = QtWidgets.QLabel(self.centralwidget)
        self.how_much_for_piece_label.setGeometry(QtCore.QRect(240, 120, 341, 20))
        self.how_much_for_piece_label.setText(
            "How much would you like to pay for one piece?")

        self.gold_label = QtWidgets.QLabel(self.centralwidget)
        self.gold_label.setGeometry(QtCore.QRect(480, 160, 341, 20))
        self.gold_label.setText(
            "gold")

        self.how_much_for_piece_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.how_much_for_piece_edit.setGeometry(QtCore.QRect(350, 160, 113, 25))

        """ MAKE OFFER PART """

        self.make_offer_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_offer_button.setGeometry(QtCore.QRect(190, 220, 271, 61))
        self.make_offer_button.setText("Make offer")

        self.setCentralWidget(self.centralwidget)

    def make_offer(self):
        """

        """
        if not self.grandparent.city.owner.granary.is_enough(self.gold_dict):
            self.no_material_type_label.setVisible(False)
            self.not_enough_label.setVisible(True)
        elif self.material_type_holder is None:
            self.not_enough_label.setVisible(False)
            self.no_material_type_label.setVisible(True)
        else:  # this happens when everything is ok and unit building starts
            self.grandparent.city.owner.granary.pay_for(self.total_cost_holder)  # paying for unit

            self.grandparent.transport_unit_building_costs(self.total_cost_holder)
            count = self.how_many_slider.value()
            print(f"Requested unit {self.unit_type_holder}")
            self.grandparent.city.unit_request = {'type': self.unit_type_holder, 'count': count}
            self.grandparent.city.days_left_to_building_completion = self.total_cost_holder["time"]

            # self.grandparent.city.show_whats_building()
            self.hide()
            self.parent.kill_app()

    def recalculate_how_many(self):
        self.how_many_edit.setText(str(self.how_many_slider.value()))

    def change_slider_from_line_edit(self):
        try:
            number = int(self.how_many_edit.text())
            if number < 1:
                number = 1
                self.how_many_edit.setText(str(number))
            elif number > 500:
                number = 500
                self.how_many_edit.setText(str(number))
        except:  # catches all strange input
            number = 1
            self.how_many_edit.setText(str(number))
        self.how_many_slider.setValue(number)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuyGoodsWindow(None, None)
    win.show()
    sys.exit(app.exec_())
