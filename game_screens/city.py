import os
import random

import arcade

from game_screens.granary import Granary


class City(arcade.sprite.Sprite):
    def __init__(self, unit, name, area):
        super().__init__(":resources:images/tiles/brickGrey.png")
        self.name = name
        self.color = unit.color
        self.tile = unit.tile
        self.tile.city = self
        self.width = self.tile.width
        self.height = self.tile.height
        self.owner = unit.owner
        self.center_x = self.tile.center_x
        self.center_y = self.tile.center_y
        self.path_to_visualization = self.get_random_city_visualization_path()

        self.area = area
        self.goods = self.calculate_goods()  # this will/is used for displaying stats of the city
        self.granary = Granary()

        self.unit_currently_being_build = None  # if no unit is being build this should be None
        self.cost_of_unit_currently_being_build = None

    def __str__(self):
        return f"City_name: {self.name}, Owner: {self.owner.nick}, Civ: {self.owner.civilisation}, Coordinates: {self.tile.coords}, Goods: {self.goods}."

    def get_city_goods_income(self):
        return self.goods

    def gather_materials(self):
        """
        Gathering materials works as follows: checking all tiles in self.area and adding appropriate values to granary.
        TODO optimization of consts

        """
        for tile in self.area:
            if tile.type == 0:
                self.granary.add_gold(1)
                self.granary.add_food(8)
            if tile.type == 1:
                self.granary.add_food(5)
                self.granary.add_wood(5)
            if tile.type == 2:
                self.granary.add_food(3)
                self.granary.add_wood(10)
            if tile.type == 3:
                self.granary.add_stone(5)

    def collect_from_city(self):
        """
        This method should be called to collect all materials from this city granary to player's master granary
        """
        self.owner.granary.insert_from(self.granary)

    def calculate_goods(self):
        return self.calculate_goods_no_city(self.area)

    @staticmethod
    def calculate_goods_no_city(area):
        goods = {'gold': 0, 'wood': 0, 'stone': 0, 'food': 0}
        for tile in area:
            if tile.type == 0:
                goods['gold'] += 1
                goods['food'] += 8
            if tile.type == 1:
                goods['food'] += 5
                goods['wood'] += 5
            if tile.type == 2:
                goods['food'] += 3
                goods['wood'] += 10
            if tile.type == 3:
                goods['stone'] += 5
        return goods

    def set_area(self, area: list):
        self.area = area
        self.goods = self.calculate_goods()

    def get_random_city_visualization_path(self):
        chosen = random.choice(os.listdir("resources/images/" + f"{self.owner.short_civ}"))
        return "resources/images/" + f"{self.owner.short_civ}/" + chosen
