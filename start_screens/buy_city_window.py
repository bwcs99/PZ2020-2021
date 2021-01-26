from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import math


class BuyCityWindow(QMainWindow):
    """
    This window is used for proposing price for city buyout.
    """

    def __init__(self, parent, grandparent):
        super(BuyCityWindow, self).__init__()
        self.resize(440, 280)
        self.setWindowTitle("City Trade")
        self.gold_dict = {"gold": 0, "wood": 0, "stone": 0,
                          "food": 0}  # this dictionary is only used for holding keep of gold, but it's used couple of times so it will be easier to declare it.
        self.parent = parent
        self.grandparent = grandparent

        self.centralwidget = QtWidgets.QWidget()

        """ HOW MUCH PART """

        self.gold_slider = QtWidgets.QSlider(self.centralwidget)
        self.gold_slider.setGeometry(QtCore.QRect(40, 80, 241, 16))
        self.gold_slider.setOrientation(QtCore.Qt.Horizontal)
        self.gold_slider.setMinimum(1)
        self.gold_slider.setMaximum(self.grandparent.city.owner.granary.gold)
        self.gold_slider.setTickInterval(
            self.grandparent.city.owner.granary.gold / 25)  # works when you click next to slider
        self.gold_slider.setSingleStep(self.grandparent.city.owner.granary.gold / 25)
        self.gold_slider.valueChanged.connect(self.recalculate_how_much_gold)
        self.gold_slider.setValue(1)

        self.gold_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.gold_edit.setGeometry(QtCore.QRect(300, 70, 113, 25))
        self.gold_edit.setText("1")
        self.gold_edit.textChanged.connect(self.change_slider_from_line_edit)  # both way changing value

        self.how_many_label = QtWidgets.QLabel(self.centralwidget)
        self.how_many_label.setGeometry(QtCore.QRect(70, 30, 350, 17))
        self.how_many_label.setText("How much would you like to pay for this city?")

        """ MAKE OFFER PART """

        self.make_offer_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_offer_button.setGeometry(QtCore.QRect(80, 180, 271, 61))
        self.make_offer_button.setText("Make offer")
        self.make_offer_button.clicked.connect(self.make_offer)

        self.setCentralWidget(self.centralwidget)

    def make_offer(self):
        """
        This method sends diplomacy message to city owner. Cost from slider or line_edit is limited by player's granary
        so no more checks are needed.
        """

        self.grandparent.top_bar.me.granary.pay_for(self.gold_dict)  # paying for materials

        # TODO Diplomacy procedure - 'buying city'
        # receiver, price, resource, quantity
        # self.grandparent.client.buy_resource(self.grandparent.city.owner.nick, self.how_much_for_piece_edit.text(),
        #                                      self.material_type_holder, self.gold_edit.text())
        city = self.grandparent.city
        receiver = city.owner.nick
        coords = city.tile.coords
        self.grandparent.client.buy_city(receiver, self.gold_dict['gold'], coords)
        self.hide()
        self.grandparent.window.back_to_game()
        self.parent.kill_app()

    def recalculate_how_much_gold(self):
        self.gold_edit.setText(str(self.gold_slider.value()))

    def calculate_total_cost(self):
        payment_cost = int(self.gold_edit.text())
        self.gold_dict["gold"] = payment_cost

    def change_slider_from_line_edit(self):
        try:
            number = int(self.gold_edit.text())
            if number < 1:
                number = 1
                self.gold_edit.setText(str(number))
            elif number > self.grandparent.city.owner.granary.gold:
                number = self.grandparent.city.owner.granary.gold
                self.gold_edit.setText(str(number))
        except:  # catches all strange input
            number = 1
            self.gold_edit.setText(str(number))
        self.gold_slider.setValue(number)
        self.calculate_total_cost()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = BuyCityWindow(None, None)
    win.show()
    sys.exit(app.exec_())
