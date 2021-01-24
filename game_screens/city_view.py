import arcade
from PyQt5.QtWidgets import QApplication
from arcade.gui import UIManager

from game_screens.city import City
from game_screens.popups import CityInfo
from start_screens.build_building_window import BuildBuildingWindow
from start_screens.build_unit_window import BuildUnitWindow


class CityView(arcade.View):
    def __init__(self, top_bar):
        super().__init__()
        self.city = None
        self.building_unit_costs = None
        self.building_building_costs = None
        self.backup = None
        self.clicked_once = False

        self.ui_manager = UIManager()
        self.app = QApplication([])
        self.top_bar = top_bar

        sidebar_top = self.top_bar.size_y + 0.05
        popup_height = 0.6
        self.city_info = CityInfo(0.3, popup_height, sidebar_top)

        left, right, _, _ = self.city_info.coords_lrtb
        center_x = (left + right) / 2
        sidebar_width = right - left
        sidebar_top += popup_height + 0.025

        relative_button_height = 0.075
        button_height = int(relative_button_height * self.window.height)

        sidebar_top += relative_button_height / 2
        self.build_unit_button = BuildUnitFlatButton(self, center_x, (1 - sidebar_top) * self.window.height,
                                                     sidebar_width, button_height)

        sidebar_top += relative_button_height + 0.025
        self.build_building_window = BuildBuildingFlatButton(self, center_x, (1 - sidebar_top) * self.window.height,
                                                             sidebar_width, button_height)

    def set_city(self, city: City):
        self.city = city

    def on_show(self):
        arcade.start_render()

        self.backup = arcade.get_viewport()
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.city_info.display(self.city)
        self.top_bar.adjust()

        self.ui_manager.add_ui_element(self.build_unit_button)
        self.ui_manager.add_ui_element(self.build_building_window)

    def on_draw(self):
        img = arcade.load_texture(f"{self.city.path_to_visualization}")
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, img)

        self.city_info.draw_background()
        self.top_bar.draw_background()
        self.clicked_once = True

    def on_hide_view(self):
        arcade.set_viewport(*self.backup)
        self.city_info.hide()
        self.ui_manager.purge_ui_elements()
        self.clicked_once = False

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
    def __init__(self, parent, center_x, center_y, width, height):
        super().__init__('New unit', center_x=center_x, center_y=center_y, width=width, height=height)
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        if self.parent.clicked_once:
            win = BuildUnitWindow(self, self.parent)
            win.show()
            self.app.exec_()
            self.parent.city_info.update()
            self.parent.top_bar.update_treasury()
            print("exited build_unit_window.")
        else:
            self.parent.clicked_once = True

    def kill_app(self):
        self.app.exit()


class BuildBuildingFlatButton(arcade.gui.UIFlatButton):
    def __init__(self, parent, center_x, center_y, width, height):
        super().__init__('New building', center_x=center_x, center_y=center_y, width=width, height=height)
        self.parent = parent
        self.app = self.parent.app

    def on_click(self):
        if self.parent.clicked_once:
            win = BuildBuildingWindow(self, self.parent)
            win.show()
            self.app.exec_()
            self.parent.city_info.update()
            self.parent.top_bar.update_treasury()
            print("exited build_building_window.")
        else:
            self.parent.clicked_once = True

    def kill_app(self):
        self.app.exit()
