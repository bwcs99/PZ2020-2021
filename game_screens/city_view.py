import sys

import arcade
from PyQt5.QtWidgets import QApplication
from arcade.gui import UIManager

from build_unit_window import BuildUnitWindow
from city import City
from popups import GranaryPopup
from welcome_window import WelcomeWindow


class CityView(arcade.View):
    def __init__(self, city: City, top_bar):
        super().__init__()
        self.city = city
        self.top_bar = top_bar
        self.granary_bar = GranaryPopup(1, 0.15, city)
        self.backup = None

        self.ui_manager = UIManager()

    def on_show(self):
        self.ui_manager.purge_ui_elements()
        arcade.start_render()
        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.top_bar.adjust()
        self.granary_bar.adjust()

        button = BuildUnitFlatButton(self, center_x=self.window.width, center_y=self.window.height)
        self.ui_manager.add_ui_element(button)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.granary_bar.draw_background()
        self.top_bar.draw_background()

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.granary_bar.hide()
        self.ui_manager.unregister_handlers()
        self.backup = None

    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol)
        if symbol == 65307:  # escape button for me TODO check for everyone
            self.window.back_to_game()
        else:
            pass

    def print_some_mess(self):
        print("IT'S ALIVE")


class BuildUnitFlatButton(arcade.gui.UIGhostFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Build Unit', center_x=center_x // 2, center_y=center_y // 3, width=250, )
        self.parent = parent

    def on_click(self):
        app = QApplication(sys.argv)
        win = BuildUnitWindow(self.parent)
        win.show()
        app.exec_()
        print("exit")
