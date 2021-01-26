from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import math


class BuyGoodsWindow(QMainWindow):
    """
    This window is used for interacting with trading goods with another player. Barter was not discovered yet,
    so you can only pay with gold for other goods.
    """

    def __init__(self, parent, grandparent):
        super(BuyGoodsWindow, self).__init__()
        self.resize(630, 320)
        self.setWindowTitle("Resource Trade")
        self.gold_dict = {"gold": 0, "wood": 0, "stone": 0,
                          "food": 0}  # this dictionary is only used for holding keep of gold, but it's used couple of times so it will be easier to declare it.
        self.material_type_holder = None

        self.parent = parent
        self.grandparent = grandparent

        self.centralwidget = QtWidgets.QWidget()

        """ RADIO BUTTONS PART """

        self.wood_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.wood_radio_button.setGeometry(QtCore.QRect(60, 50, 112, 23))
        self.wood_radio_button.setText("Wood")
        self.wood_radio_button.material = "Wood"
        self.wood_radio_button.clicked.connect(self.choose_material)

        self.stone_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.stone_radio_button.setGeometry(QtCore.QRect(60, 100, 112, 23))
        self.stone_radio_button.setText("Stone")
        self.stone_radio_button.material = "Stone"
        self.stone_radio_button.clicked.connect(self.choose_material)

        self.food_radio_button = QtWidgets.QRadioButton(self.centralwidget)
        self.food_radio_button.setGeometry(QtCore.QRect(60, 150, 112, 23))
        self.food_radio_button.setText("Food")
        self.food_radio_button.material = "Food"
        self.food_radio_button.clicked.connect(self.choose_material)

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
        self.how_much_for_piece_edit.setText("1.0")
        self.how_much_for_piece_edit.textChanged.connect(self.change_one_piece_cost)

        """ MAKE OFFER PART """

        self.total_cost_label = QtWidgets.QLabel(self.centralwidget)
        self.total_cost_label.setGeometry(QtCore.QRect(60, 225, 241, 50))
        self.total_cost_label.setText("Together it's 1 gold.")

        self.make_offer_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_offer_button.setGeometry(QtCore.QRect(245, 220, 271, 61))
        self.make_offer_button.setText("Make offer")
        self.make_offer_button.clicked.connect(self.make_offer)

        """ INVISIBLE LABELS """

        self.not_enough_label = QtWidgets.QLabel(self.centralwidget)
        self.not_enough_label.setGeometry(QtCore.QRect(180, 190, 300, 21))
        self.not_enough_label.setText("You don't have enough gold to pay for that.")
        self.not_enough_label.setStyleSheet("color: rgb(255, 77, 77);")
        self.not_enough_label.setVisible(False)

        self.no_material_type_label = QtWidgets.QLabel(self.centralwidget)
        self.no_material_type_label.setGeometry(QtCore.QRect(170, 190, 400, 21))
        self.no_material_type_label.setText(
            "Choose which material you want to buy.")
        self.no_material_type_label.setStyleSheet("color: rgb(32,178,170);")
        self.no_material_type_label.setVisible(False)

        self.setCentralWidget(self.centralwidget)

    def choose_material(self):
        """
        Here material is being chosen.
        """
        radio_button = self.sender()
        if radio_button.material == self.wood_radio_button.material:
            self.material_type_holder = "Wood"
        if radio_button.material == self.stone_radio_button.material:
            self.material_type_holder = "Stone"
        if radio_button.material == self.food_radio_button.material:
            self.material_type_holder = "Food"

    def make_offer(self):
        """
        This method calculates total cost of trade request ( ceiling(how_many_pieces * how_much_for_piece) ).
        And checks if it's alright, when it is, diplomacy procedure for 'buying materials' is called.
        """
        if not self.grandparent.city.owner.granary.is_enough(self.gold_dict):
            self.no_material_type_label.setVisible(False)
            self.not_enough_label.setVisible(True)
        elif self.material_type_holder is None:
            self.not_enough_label.setVisible(False)
            self.no_material_type_label.setVisible(True)
        else:  # this happens when everything is ok
            self.grandparent.top_bar.me.granary.pay_for(self.gold_dict)  # paying for materials

            # TODO Diplomacy procedure - 'buying materials'
            # receiver, price, resource, quantity
            self.grandparent.client.buy_resource(self.grandparent.city.owner.nick, self.how_much_for_piece_edit.text(),
                                                 self.material_type_holder, self.how_many_edit.text())

            self.hide()
            self.grandparent.window.back_to_game()
            self.parent.kill_app()

    def recalculate_how_many(self):
        self.how_many_edit.setText(str(self.how_many_slider.value()))

    def calculate_total_cost(self):
        payment_cost = math.ceil(float(self.how_much_for_piece_edit.text()) * int(self.how_many_edit.text()))
        self.total_cost_label.setText(f"Together it's {payment_cost} gold.")
        self.gold_dict["gold"] = payment_cost

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
        self.calculate_total_cost()

    def change_one_piece_cost(self):
        try:
            cost = float(self.how_much_for_piece_edit.text())
            if cost < 0.0:
                cost = 0.1
                self.how_much_for_piece_edit.setText(str(cost))
            elif cost > 100.0:
                cost = 100.0
                self.how_much_for_piece_edit.setText(str(cost))
        except:  # catches all strange input
            cost = 1.0
            self.how_much_for_piece_edit.setText(str(cost))
        self.calculate_total_cost()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuyGoodsWindow(None, None)
    win.show()
    sys.exit(app.exec_())
