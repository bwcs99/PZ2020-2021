import arcade
from PyQt5.QtWidgets import QApplication
from arcade.gui import UIManager

from game_screens.city import City
from game_screens.popups import GranaryPopup
from start_screens.build_building_window import BuildBuildingWindow
from start_screens.build_unit_window import BuildUnitWindow


class EnemyCityView(arcade.View):
    def __init__(self, top_bar):
        super().__init__()
        self.city = None
        self.app = QApplication([])
        self.top_bar = top_bar
        self.backup = None
        self.ui_manager = UIManager()
        self.buy_city_button = None
        self.buy_goods_button = None

    def set_city(self, city: City):
        self.city = city

    def on_show(self):
        arcade.start_render()

        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.top_bar.adjust()

        self.buy_city_button = BuyCityButton(self, center_x=self.window.width, center_y=self.window.height)
        self.ui_manager.add_ui_element(self.buy_city_button)
        self.buy_goods_button = BuyGoodsButton(self, center_x=self.window.width,
                                               center_y=self.window.height)
        self.ui_manager.add_ui_element(self.buy_goods_button)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.top_bar.draw_background()

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.ui_manager.purge_ui_elements()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.back_to_game()
        else:
            pass


class BuyCityButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Buy this city', center_x=center_x // 2 - 300, center_y=center_y // 4, width=250, )

    def on_click(self):
        print("Buying city procedure")


class BuyGoodsButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Buy goods', center_x=center_x // 2 + 300, center_y=center_y // 4, width=250, )
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        win = BuyGoodsWindow(self, self.parent)
        win.show()
        self.app.exec_()
        print("exited buy goods.")

    def kill_app(self):
        self.app.exit()
