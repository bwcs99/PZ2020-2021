from copy import copy

import arcade

from city import City
from game_screens.units import Settler

BACKGROUND_COLOR = arcade.color.ST_PATRICK_BLUE
FONT_COLOR = arcade.color.WHITE


class PopUp(arcade.gui.UIManager):
    """
    An abstract class representing a pop-up window.
    """

    def __init__(self, left: float, bottom: float, size_x: float, size_y: float, background_color=BACKGROUND_COLOR):
        """
        :param left: The popup's left margin expressed as a percentage of current screen width, between 0 and 1.
        :param bottom: The popup's bottom margin expressed as a percentage of current screen height, between 0 and 1.
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and (1 - left).
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and (1 - right).
        """
        super().__init__()

        self.width = None
        self.height = None
        self.coords_lrtb = None

        self.size_x = size_x
        self.size_y = size_y
        self.left = left
        self.bottom = bottom
        self.background_color = background_color

        self.adjust_coords()
        self.hitbox = copy(self.coords_lrtb)

    def adjust_coords(self):
        """ Adjusts the coords of the pop-up to the current screen borders. """
        left, right, bottom, top = arcade.get_viewport()
        width = right - left
        height = top - bottom
        self.width = self.size_x * width
        self.height = self.size_y * height
        left += self.left * width
        bottom += self.bottom * height
        self.coords_lrtb = (left, left + self.width, bottom + self.height, bottom)

    def draw_background(self):
        """ Draws the background rectangle for the pop-up if it's visible. """
        if self.visible():
            arcade.draw_lrtb_rectangle_filled(*self.coords_lrtb, self.background_color)

    def is_hit(self, x, y):
        """
        Checks whether the pop-up has been clicked
        :param x: The x coord of the click, relative to the current screen size.
        :param y: The y coord of the click, relative to the current screen size.
        """
        if not self.visible():
            return False
        left, right, top, bottom = self.hitbox
        return left <= x <= right and bottom <= y <= top

    def visible(self):
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, button, modifiers):
        pass


class TopBar(PopUp):
    """
    A representation of the game window's top bar containing info about the player's treasury and the name of the
    player whose turn is currently taking place. Holds and updates the current position of the bar on the screen.
    """

    def __init__(self, size: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size: Should be between 0 and 1. Determines what part of the current screen height should the bar occupy.
        """
        super().__init__(0, 1 - size, 1, size, background_color)

        self.money_label = arcade.gui.UILabel("Treasury: 0 (+0)", 0, 0)
        self.money_label.color = font_color
        self.time_label = arcade.gui.UILabel("Press SPACE to end turn (5:00)", 0, 0)
        self.time_label.color = font_color
        self.adjust()
        self.max_height = self.height
        self.add_ui_element(self.money_label)
        self.add_ui_element(self.time_label)

    def adjust(self):
        """
        Adjusts the coords of the bar and its elements to the current screen borders.
        """
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        self.money_label.center_y = self.time_label.center_y = top - self.height / 2
        self.money_label.height = self.time_label.height = 0.4 * self.height
        self.money_label.center_x = left + 0.125 * self.width
        self.time_label.center_x = left + 0.775 * self.width
        self.money_label.width = len(self.money_label.text) / 75 * self.width
        self.time_label.width = len(self.time_label.text) / 75 * self.width

    def turn_change(self, nick: str = None):
        """
        Changes the label to reflect the player whose turn is taking place. No nick should be provided if it's the
        turn of the player running the client.
        """
        if nick:
            self.time_label.text = f"{nick}'s turn (5:00)"
        else:
            self.time_label.text = "Press SPACE to end turn (5:00)"
        self.adjust()


class UnitPopup(PopUp):
    """
    A bottom left corner pop-up that appears after clicking on a unit and contains its stats.
    """

    def __init__(self, size_x: float, size_y: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0, 0, size_x, size_y, background_color)

        self.owner_label = arcade.gui.UILabel("", 0, 0)
        self.action_label = arcade.gui.UILabel("", 0, 0)
        self.health_label = arcade.gui.UILabel("", 0, 0)
        self.health_label.color = font_color
        self.move_label = arcade.gui.UILabel("", 0, 0)
        self.move_label.color = font_color
        self.unit = None
        self.is_unit_mine = False
        self.adjust()

    def display(self, unit, mine: bool):
        """ Attaches a unit to the pop-up and makes it visible. """
        self.hide()
        self.unit = unit
        self.add_ui_element(self.owner_label)
        self.add_ui_element(self.action_label)
        self.add_ui_element(self.health_label)
        self.add_ui_element(self.move_label)
        self.is_unit_mine = mine
        self.update()

    def update(self):
        """ Updates the labels with the current state of the attached unit. """
        if self.visible():
            self.owner_label.text = str(self.unit)
            self.action_label.text = "(Press N to build a city)" if self.can_build_city() else ""
            self.health_label.text = f"Health: {f'{self.unit.health}%'.rjust(10, ' ')}"
            self.move_label.text = f"Movement: {f'{self.unit.movement}/{self.unit.max_movement}'.rjust(7, ' ')}"
            self.adjust()

    def hide(self):
        """ Detaches the unit and hides the pop-up. """
        self.purge_ui_elements()
        self.unit = None

    def hide_if_on_tile(self, x, y):
        """
        Hides the pop-up if the unit it references is located on the tile (x, y). Useful for when opponent's settlers
        build a city.
        """
        if self.unit and self.unit.tile.coords == (x, y):
            self.hide()

    def visible(self):
        """ Determines if the pop-up is visible. Used in hit box and drawing."""
        return self.unit is not None

    def can_build_city(self):
        """ Determines whether to show the message that a settler can build a city. """
        return self.is_unit_mine and type(self.unit) == Settler and self.visible()

    def adjust(self):
        """
        Adjusts the coords of the pop-up and its elements to the current screen borders.
        """
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        self.health_label.center_y = bottom + self.height / 5
        self.move_label.center_y = bottom + 2 * self.height / 5
        self.health_label.height = self.move_label.height = self.action_label.height = 0.1 * self.height
        self.owner_label.height = 0.2 * self.height
        self.health_label.center_x = self.move_label.center_x = self.owner_label.center_x = self.action_label.center_x = left + 0.5 * self.width
        self.health_label.width = self.move_label.width = self.owner_label.width = self.action_label.width = 0.8 * self.width
        if self.action_label.text:
            self.owner_label.center_y = top - self.height / 5
            self.action_label.center_y = top - 1.75 * self.height / 5
        else:
            self.owner_label.center_y = top - 1.5 * self.height / 5


class GranaryPopup(PopUp):
    """
    Popup used in the CityView for showing city Granary info.
    """

    def __init__(self, size_x: float, size_y: float, city: City, background_color=BACKGROUND_COLOR,
                 font_color=FONT_COLOR):
        """
        :param size: Should be between 0 and 1. Determines what part of the current screen height should the bar occupy.
        """
        super().__init__(0, 0, size_x, size_y, background_color)
        self.city = city
        pretty_goods = ""
        for key in self.city.get_city_goods_income():
            pretty_goods += str(key) + ": " + str(self.city.get_city_goods_income()[key]) + ", "
        self.materials_label = arcade.gui.UILabel(f"This city produces {pretty_goods} Master.", 0, 0)
        self.materials_label.color = font_color
        self.adjust()
        self.max_height = self.height
        self.add_ui_element(self.materials_label)

    def adjust(self):
        """
        Adjusts the coords of the bar and its elements to the current screen borders.
        """
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        self.materials_label.center_y = bottom + self.height / 2
        self.materials_label.center_x = left + 0.5 * self.width
        self.materials_label.height = 0.5 * self.height
        self.materials_label.width = 0.8 * self.width

    def hide(self):
        """ Detaches the unit and hides the pop-up. """
        self.purge_ui_elements()
