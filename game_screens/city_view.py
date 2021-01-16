import sys

import arcade
from PyQt5.QtWidgets import QApplication
from arcade.gui import UIManager

from game_screens.city import City
from game_screens.popups import GranaryPopup
from start_screens.build_building_window import BuildBuildingWindow
from start_screens.build_unit_window import BuildUnitWindow


# TODO: Display info about currently building object in the city. Think about units AND city upgrades.
# TODO: Add displaying city name
# TODO: Add displaying built buildings

class CityView(arcade.View):
    def __init__(self, top_bar):
        super().__init__()
        self.city = None
        self.building_unit_costs = None
        self.building_building_costs = None
        self.app = QApplication([])
        self.top_bar = top_bar
        self.granary_bar = None
        self.backup = None
        self.ui_manager = UIManager()
        self.build_unit_button = None
        self.build_building_window = None

    def set_city(self, city: City):
        self.city = city
        self.granary_bar = GranaryPopup(1, 0.15, city)

    def on_show(self):
        arcade.start_render()

        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.top_bar.adjust()
        self.granary_bar.adjust()

        # del self.button

        self.build_unit_button = BuildUnitFlatButton(self, center_x=self.window.width, center_y=self.window.height)
        self.ui_manager.add_ui_element(self.build_unit_button)
        self.build_building_window = BuildBuildingFlatButton(self, center_x=self.window.width,
                                                             center_y=self.window.height)
        self.ui_manager.add_ui_element(self.build_building_window)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)
        self.granary_bar.draw_background()
        self.top_bar.draw_background()

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.granary_bar.hide()
        self.ui_manager.purge_ui_elements()
        # self.backup = None

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.back_to_game()
        else:
            pass

    def transport_unit_building_costs(self, total_costs):
        """
        This method is called by BuildUnitWindow. This name should NOT be changed.
        """
        self.building_unit_costs = total_costs
        print("Building unit costs: ", self.building_unit_costs)

    def transport_building_building_costs(self, building_costs):
        """
        This method is called by BuildUnitWindow. This name should NOT be changed.
        """
        self.building_building_costs = building_costs
        print("Building building costs: ", self.building_building_costs)


class BuildUnitFlatButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Build Unit', center_x=center_x // 2 - 300, center_y=center_y // 4, width=250, )
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        win = BuildUnitWindow(self, self.parent)
        win.show()
        self.app.exec_()
        print("exited build_unit_window.")

    def kill_app(self):
        self.app.exit()


class BuildBuildingFlatButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y):
        super().__init__('Build Building', center_x=center_x // 2 + 300, center_y=center_y // 4, width=250, )
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        win = BuildBuildingWindow(self, self.parent)
        win.show()
        self.app.exec_()
        print("exited build_building_window.")

    def kill_app(self):
        self.app.exit()
