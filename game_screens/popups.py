from copy import copy
import random

import arcade
import arcade.gui

from game_screens.city import City
from game_screens.combat.garrison import Garrison
from game_screens.units import Settler
from game_screens.granary import Granary
from player import Player

BACKGROUND_COLOR = (60, 0, 0)  # arcade.color.ST_PATRICK_BLUE
FONT_COLOR = arcade.color.WHITE

arcade.gui.elements.UIStyle.set_class_attrs(
    arcade.gui.elements.UIStyle.default_style(),
    "label",
    font_name="resources/fonts/november",
    font_color=FONT_COLOR,
    font_size=64
)

arcade.gui.elements.UIStyle.set_class_attrs(
    arcade.gui.elements.UIStyle.default_style(),
    "flatbutton",
    font_name="resources/fonts/november",
    font_color=FONT_COLOR,
    bg_color=BACKGROUND_COLOR
)


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

    def __init__(self, me: Player or None, size: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size: Should be between 0 and 1. Determines what part of the current screen height should the bar occupy.
        """
        super().__init__(0, 1 - size, 1, size, background_color)
        self.me = me
        self.treasury_label = arcade.gui.UILabel("Treasury: 0 (+0)", 0, 0)
        self.treasury_label.color = font_color
        self.time_label = arcade.gui.UILabel("Press SPACE to end turn (5:00)", 0, 0)
        self.time_label.color = font_color
        self.adjust()
        self.max_height = self.height
        self.add_ui_element(self.treasury_label)
        self.add_ui_element(self.time_label)
        self.ended = False

    def adjust(self):
        """
        Adjusts the coords of the bar and its elements to the current screen borders.
        """
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        self.treasury_label.center_y = self.time_label.center_y = top - self.height / 2
        self.treasury_label.height = self.time_label.height = 0.4 * self.height
        self.treasury_label.width = len(self.treasury_label.text) / 100 * self.width
        self.time_label.width = len(self.time_label.text) / 100 * self.width
        self.treasury_label.center_x = left + 0.025 * self.width + 0.5 * self.treasury_label.width
        self.time_label.center_x = right - 0.025 * self.width - 0.5 * self.time_label.width

    def turn_change(self, nick: str = None):
        """
        Changes the label to reflect the player whose turn is taking place. No nick should be provided if it's the
        turn of the player running the client.
        """
        if self.ended:
            return
        if nick:
            self.time_label.text = f"{nick}'s turn"
        else:
            self.time_label.text = "Press SPACE to end turn"
        self.adjust()

    def update_treasury(self):
        total = self.me.granary
        change = {res: 0 for res in ['gold', 'wood', 'food', 'stone']}
        for city in self.me.cities:
            change['gold'] += city.goods['gold']
            change['wood'] += city.goods['wood']
            change['food'] += city.goods['food']
            change['stone'] += city.goods['stone']

        self.treasury_label.text = "G:{} (+{}), W:{} (+{}), S:{} (+{}), F:{} (+{})".format(total.gold,
                                                                                           change["gold"],
                                                                                           total.wood,
                                                                                           change["wood"],
                                                                                           total.stone,
                                                                                           change["stone"],
                                                                                           total.food,
                                                                                           change["food"])
        self.adjust()

    def game_ended(self):
        self.time_label.text = "The game is finished"
        self.ended = True
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
        self.owner_label.color = font_color

        self.action_label = arcade.gui.UILabel("", 0, 0)
        self.action_label.color = font_color

        self.move_label = arcade.gui.UILabel("", 0, 0)
        self.move_label.color = font_color

        self.health_label = arcade.gui.UILabel("", 0, 0)
        self.health_label.color = font_color

        self.unit = None
        self.is_unit_mine = False
        self.adjust()

    def display(self, unit, mine: bool):
        """ Attaches a unit to the pop-up and makes it visible. """
        self.hide()
        self.unit = unit
        self.add_ui_element(self.owner_label)
        self.add_ui_element(self.action_label)
        self.add_ui_element(self.move_label)
        self.add_ui_element(self.health_label)
        self.is_unit_mine = mine
        self.update()

    def update(self):
        """ Updates the labels with the current state of the attached unit. """
        if self.visible():
            self.owner_label.text = str(self.unit)
            if type(self.unit) == Garrison:
                self.action_label.text = f"Strength: {f'{self.unit.damage}'.rjust(7, ' ')}"
            elif self.can_build_city():
                self.action_label.text = "(Press N to build a city)"
            else:
                self.action_label.text = ""

            self.move_label.text = f"Movement: {f'{self.unit.movement}/{self.unit.max_movement}'.rjust(7, ' ')}"
            self.health_label.text = f"Health: {f'{self.unit.health} HP'.rjust(10, ' ')}"
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
        return self.is_unit_mine and not self.unit.tile.owner and type(self.unit) == Settler and self.visible()

    def adjust(self):
        """
        Adjusts the coords of the pop-up and its elements to the current screen borders.
        """
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / 6
        self.owner_label.center_y = top - 1.25 * base_height
        self.action_label.center_y = bottom + base_height
        self.health_label.center_y = bottom + 2 * base_height
        self.move_label.center_y = bottom + 3 * base_height

        self.owner_label.height = 0.15 * self.height
        self.move_label.height = self.health_label.height = self.action_label.height = 0.1 * self.height

        self.owner_label.center_x = left + 0.5 * self.width
        self.move_label.center_x = self.health_label.center_x = self.action_label.center_x = self.owner_label.center_x

        self.owner_label.width = 0.8 * self.width
        self.move_label.width = self.health_label.width = self.action_label.width = self.owner_label.width


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
        self.purge_ui_elements()


class CityCreationPopup(PopUp):
    """
    A pop-up shown on city creation. Allows to see potential city stats and change the city name.
    """
    MAX_NAME_LEN = 20

    def __init__(self, size_x: float, size_y: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0.5 * (1 - size_x), 0.5 * (1 - size_y), size_x, size_y, background_color)

        self.top_label = arcade.gui.UILabel("New city", 0, 0)
        self.name_input = arcade.gui.UILabel("Name", 0, 0)
        self.name_input.focused = True
        self.gold_label = arcade.gui.UILabel("Gold: +", 0, 0)
        self.food_label = arcade.gui.UILabel("Food: +", 0, 0)
        self.wood_label = arcade.gui.UILabel("Wood: +", 0, 0)
        self.stone_label = arcade.gui.UILabel("Stone: +", 0, 0)
        self.cancel_label = arcade.gui.UILabel("ENTER: accept, ESC: cancel", 0, 0)
        self.all_elements = [self.top_label, self.name_input, self.gold_label, self.food_label, self.wood_label,
                             self.stone_label, self.cancel_label]
        for element in self.all_elements:
            element.color = font_color
        self.tile = None
        self.stats = None
        self.n_pressed = False  # to stop adding the initial N press to the name
        self.adjust()

    def display(self, unit, stats):
        """ Attaches a unit and potential stats to the pop-up and makes it visible. """
        self.hide()
        self.tile = unit.tile
        self.stats = stats
        for element in self.all_elements:
            self.add_ui_element(element)
        self.update()

    def update(self):
        """ Updates the labels with potential stats of the new city. """
        if self.visible():
            self.name_input.text = self.get_random_city_name()
            self.gold_label.text = "Gold: " + f"+{self.stats['gold']}".rjust(10, ' ')
            self.food_label.text = "Food: " + f"+{self.stats['food']}".rjust(10, ' ')
            self.wood_label.text = "Wood: " + f"+{self.stats['wood']}".rjust(10, ' ')
            self.stone_label.text = "Stone: " + f"+{self.stats['stone']}".rjust(9, ' ')
            self.adjust()

    def hide(self):
        """ Wipes the pop-up's data and hides it. """
        self.purge_ui_elements()
        self.tile = None
        self.stats = None
        self.n_pressed = False
        return self.name_input.text

    def visible(self):
        return self.tile is not None

    def adjust(self):
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / 12
        for element in self.all_elements:
            element.center_x = left + 0.5 * self.width
            element.width = 0.8 * self.width
            element.height = base_height

        self.top_label.width = 0.6 * self.width
        self.name_input.width = len(self.name_input.text) * 0.8 * self.width / self.MAX_NAME_LEN
        self.top_label.center_y = top - self.height / 12
        self.name_input.center_y = top - 3.5 * self.height / 12
        self.gold_label.center_y = top - 6 * self.height / 12
        self.food_label.center_y = top - 7 * self.height / 12
        self.wood_label.center_y = top - 8 * self.height / 12
        self.stone_label.center_y = top - 9 * self.height / 12
        self.cancel_label.center_y = top - 11 * self.height / 12

    def get_random_city_name(self):
        """
        It's like 80 or 90 city names. This method returns random from this list.
        """

        names_list = ["Stewart Manor", "Montour", "Ivalee", "Frost", "Guaynabo", "Oak Beach", "Elk Mountain",
                      "Paragon Estates", "Malin", "Deatsville", "South El Monte", "San Rafael", "Warfield", "Gilboa",
                      "Fuquay", "Lucedale", "Matherville", "Faunsdale", "Waller", "Islandton", "Big Lake", "Macon",
                      "Speed", "Hawthorn Woods", "St. Hedwig", "Sidney", "Cliff", "Sunset", "Bolan", "Tobaccoville",
                      "Kiryas Joel", "Kokomo", "Forest Lake", "Barboursville", "Shawneetown", "Meridian Station",
                      "Maribel", "Millerville", "Wolf Lake", "Village Green", "Romeoville", "Whiteriver", "Palatka",
                      "South Pittsburg", "La Grange Park", "Sekiu", "Tillmans Corner", "Tselakai Dezza",
                      "Berlin Heights", "Twin Lakes", "Sruron", "Misall", "Efruiphia", "Klordon", "Huwell", "Granta",
                      "Trury", "Zhose", "Ouverta", "Ouiswell", "Vlutfast", "Ureuycester", "Madford", "Vlagate",
                      "Crerset", "Shosa", "Ploni", "Certon", "Agoscester", "Estervine", "Nekmouth", "Glawell", "Hason",
                      "Cehson", "Glebert", "Qark", "Pila", "Aklery", "Arkginia", "Illeby", "Ubrukdiff", "Claason",
                      "Agutin", "Yihmery", "Mehull", "Oshares", "Izhont", "Ylin", "Oniover", "Urgstin"]
        return random.choice(names_list)

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.n_pressed:
            self.n_pressed = True
        elif self.visible() and symbol != arcade.key.ENTER and symbol != arcade.key.ESCAPE:
            if symbol == arcade.key.BACKSPACE:
                self.name_input.text = self.name_input.text[:-1]
            else:
                letter = chr(symbol)
                if len(self.name_input.text) < self.MAX_NAME_LEN and (letter.isalpha() or letter == ' '):
                    self.name_input.text += letter.upper() if modifiers & arcade.key.MOD_SHIFT else letter
            self.adjust()


class EndingPopup(PopUp):
    """
    A pop-up that shows up after the game has ended. It shows the final ranking.
    """
    MAX_USERNAME_LENGTH = 17

    def __init__(self, size_x: float, size_y: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0.5 * (1 - size_x), 0.5 * (1 - size_y), size_x, size_y, background_color)

        self.top_label = arcade.gui.UILabel("Final ranking", 0, 0)
        self.top_label.color = font_color
        self.players = [arcade.gui.UILabel("", 0, 0) for _ in range(4)]
        self.ranking = None
        for player in self.players:
            player.color = font_color
        self.bottom_label = arcade.gui.UILabel("Press ESC to view the map", 0, 0)
        self.adjust()

    def display(self, ranking):
        """ Attaches a ranking to the pop-up and makes it visible. """
        self.hide()
        self.ranking = sorted(ranking, key=lambda x: x[1])
        self.add_ui_element(self.top_label)
        self.add_ui_element(self.bottom_label)
        for player in self.players:
            self.add_ui_element(player)
        self.update()

    def update(self):
        if self.visible():
            for i, (player, rank) in enumerate(self.ranking):
                if len(player) > self.MAX_USERNAME_LENGTH:
                    player = player[:self.MAX_USERNAME_LENGTH - 3]
                    player += "..."
                self.players[i].text = f"{rank}. {player}"
            self.adjust()

    def hide(self):
        """ Hides the pop-up. """
        self.ranking = None
        self.purge_ui_elements()

    def visible(self):
        return self.ranking is not None

    def adjust(self):
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / 9
        self.top_label.width = self.bottom_label.width = 0.8 * self.width
        self.top_label.height = self.bottom_label.height = base_height
        self.top_label.center_x = self.bottom_label.center_x = left + 0.5 * self.width
        self.top_label.center_y = top - base_height
        self.bottom_label.center_y = bottom + base_height
        for i, player in enumerate(self.players):
            player.width = len(player.text) * 0.8 * self.width / (self.MAX_USERNAME_LENGTH + 3)
            player.center_x = left + 0.1 * self.width + 0.5 * player.width
            player.height = 0.8 * base_height
            player.center_y = top - (i + 3) * base_height

    def on_key_press(self, symbol: int, modifiers: int):
        if self.visible() and symbol == arcade.key.ESCAPE:
            self.hide()


class CityInfo(PopUp):
    """
    A pop-up that shows up in city view.
    """

    def __init__(self, size_x: float, size_y: float, top: float, background_color=BACKGROUND_COLOR,
                 font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0.95 * (1 - size_x), 1 - (top + size_y), size_x, size_y, background_color)
        self.city = None
        self.base_width = None

        self.name_label = arcade.gui.UILabel("City", 0, 0)
        self.gold_label = arcade.gui.UILabel("Gold: +", 0, 0)
        self.food_label = arcade.gui.UILabel("Food: +", 0, 0)
        self.wood_label = arcade.gui.UILabel("Wood: +", 0, 0)
        self.stone_label = arcade.gui.UILabel("Stone: +", 0, 0)
        self.top_part = [self.name_label, self.gold_label, self.food_label, self.wood_label, self.stone_label]

        self.cur_top_label = arcade.gui.UILabel("Current construction:", 0, 0)
        self.current_label = arcade.gui.UILabel("Nothing", 0, 0)
        self.mid_part = [self.cur_top_label, self.current_label]

        self.constructed_label = arcade.gui.UILabel("Already built:", 0, 0)
        self.buildings = [arcade.gui.UILabel("", 0, 0) for _ in range(5)]
        self.bottom_part = [self.constructed_label, *self.buildings]

        self.all_elements = [*self.top_part, *self.mid_part, *self.bottom_part]
        for el in self.all_elements:
            el.color = font_color

        self.adjust()

    def display(self, city):
        """ Attaches a city to the pop-up and makes it visible. """
        self.hide()
        self.city = city
        for el in self.all_elements:
            self.add_ui_element(el)
        self.update()

    def update(self):
        if self.visible():
            self.name_label.text = self.city.name
            stats = self.city.goods
            self.gold_label.text = "Gold:" + f"+{stats['gold']}".rjust(self.base_width - 5, ' ')
            self.food_label.text = "Food:" + f"+{stats['food']}".rjust(self.base_width - 5, ' ')
            self.wood_label.text = "Wood:" + f"+{stats['wood']}".rjust(self.base_width - 5, ' ')
            self.stone_label.text = "Stone:" + f"+{stats['stone']}".rjust(self.base_width - 6, ' ')

            if self.city.unit_request:
                self.current_label.text = f"{self.city.unit_request['count']} {self.city.unit_request['type']} ({self.city.days_left_to_building_completion})"
            elif self.city.building_request:
                self.current_label.text = f"{self.city.building_request} ({self.city.days_left_to_building_building_completion})"
            else:
                self.current_label.text = "Nothing"

            i = 0
            for building, built in self.city.buildings.items():
                if built:
                    self.buildings[i].text = building
                    i += 1

            self.adjust()

    def hide(self):
        """ Hides the pop-up. """
        self.city = None
        self.purge_ui_elements()

    def visible(self):
        return self.city is not None

    def adjust(self):
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / (len(self.all_elements) + 5)
        self.base_width = max(len(el.text) for el in self.all_elements)

        for element in self.all_elements:
            element.width = len(element.text) * 0.8 * self.width / self.base_width
            element.center_x = left + 0.1 * self.width + 0.5 * element.width
            element.height = 0.8 * base_height

        shift = 1
        for part in [self.top_part, self.mid_part, self.bottom_part]:
            shift += 1
            for element in part:
                element.center_y = top - shift * base_height
                shift += 1

        self.name_label.center_x = (left + right) / 2
        self.name_label.center_y = top - base_height


class EnemyCityInfo(PopUp):
    """
    A pop-up that shows up in enemy city view.
    """

    def __init__(self, size_x: float, size_y: float, top: float, background_color=BACKGROUND_COLOR,
                 font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0.95 * (1 - size_x), 1 - (top + size_y), size_x, size_y, background_color)
        self.city = None

        self.name_label = arcade.gui.UILabel("City", 0, 0)
        self.civ_label = arcade.gui.UILabel("Civ", 0, 0)
        self.player_label = arcade.gui.UILabel("Nick", 0, 0)

        self.all_elements = [self.name_label, self.civ_label, self.player_label]
        for el in self.all_elements:
            el.color = font_color

        self.adjust()

    def display(self, city):
        """ Attaches a city to the pop-up and makes it visible. """
        self.hide()
        self.city = city
        for el in self.all_elements:
            self.add_ui_element(el)
        self.update()

    def update(self):
        if self.visible():
            self.name_label.text = self.city.name
            self.civ_label.text = self.city.owner.civilisation
            self.player_label.text = self.city.owner.nick
            self.adjust()

    def hide(self):
        """ Hides the pop-up. """
        self.city = None
        self.purge_ui_elements()

    def visible(self):
        return self.city is not None

    def adjust(self):
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / (len(self.all_elements) + 1)
        center = (right + left) / 2
        base_width = max(len(el.text) for el in self.all_elements)

        for i, element in enumerate(self.all_elements):
            element.width = len(element.text) * 0.8 * self.width / base_width
            element.center_y = top - (i + 1) * base_height
            element.center_x = center
            element.height = 0.8 * base_height


class DiplomaticPopup(PopUp):
    """
    A pop-up containing a diplomatic notification. Displayed at the start of a player's turn.
    """

    def __init__(self, size_x: float, size_y: float, background_color=BACKGROUND_COLOR, font_color=FONT_COLOR):
        """
        :param size_x: The popup's width expressed as a percentage of current screen width, between 0 and 1.
        :param size_y: The popup's height expressed as a percentage of current screen height, between 0 and 1.
        """
        super().__init__(0.5 * (1 - size_x), 0.5 * (1 - size_y), size_x, size_y, background_color)

        self.top_label = arcade.gui.UILabel("Message from ...", 0, 0)
        self.message_label = arcade.gui.UILabel("", 0, 0)
        self.cancel_label = arcade.gui.UILabel("Press ENTER to continue", 0, 0)
        self.all_elements = [self.top_label, self.message_label, self.cancel_label]
        for element in self.all_elements:
            element.color = font_color
        self.visible = False
        self.rejectable = False
        self.adjust()

    def display(self, message, sender, rejectable=False):
        """ Attaches a unit and potential stats to the pop-up and makes it visible. """
        self.hide()
        self.visible = True
        self.rejectable = True
        for element in self.all_elements:
            self.add_ui_element(element)
        self.top_label.text = f"Message from {sender}"
        self.message_label.text = message
        self.cancel_label.text = "ENTER: accept, ESC: reject" if rejectable else "Press ENTER to continue"
        self.adjust()

    def hide(self):
        """ Wipes the pop-up's data and hides it. """
        self.purge_ui_elements()
        self.visible = False

    def adjust(self):
        self.adjust_coords()
        left, right, top, bottom = self.coords_lrtb
        base_height = self.height / 12
        for element in self.all_elements:
            element.center_x = left + 0.5 * self.width
            element.width = 0.8 * self.width
            element.height = base_height

        self.top_label.width = 0.6 * self.width
        self.top_label.center_y = top - self.height / 12
        self.message_label.center_y = top - 3.5 * self.height / 12
        self.cancel_label.center_y = top - 11 * self.height / 12

    def on_key_press(self, symbol: int, modifiers: int):
        if self.visible:
            if self.rejectable:
                if symbol == arcade.key.ENTER:
                    self.hide()
                elif symbol == arcade.key.ESCAPE:
                    self.hide()
            elif symbol == arcade.key.ENTER:
                self.hide()
