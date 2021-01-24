import os
import random

import arcade

from game_screens.granary import Granary


class City(arcade.sprite.Sprite):
    def __init__(self, unit, name, area):
        self.owner = unit.owner

        super().__init__(f"resources/sprites/cities/{self.owner.short_civ}_city.png")
        self.name = name
        self.color = unit.color
        self.tile = unit.tile
        self.tile.city = self
        self.width = self.tile.width
        self.height = self.tile.height
        self.center_x = self.tile.center_x
        self.center_y = self.tile.center_y
        self.path_to_visualization = self.get_random_city_visualization_path()

        self.area = area
        self.granary = Granary()

        self.unit_request = None  # if no unit is being build this should be None
        self.building_request = None

        # self.enhanced_area_registered = False  # a bool to prevent multiple area recalculations
        self.current_radius = 1
        self.age_since_tower = 0
        self.next_age_threshold = 1
        self.buildings = {"Astronomic Tower": False, "Mines": False, "Free Market": False, "Armory": False,
                          "Passiflora": False}
        self.goods = self.calculate_goods()  # this will/is used for displaying stats of the city

        self.days_left_to_building_completion = 0
        self.days_left_to_building_building_completion = 0

    def __str__(self):
        return f"City_name: {self.name}, Owner: {self.owner.nick}, " \
               f"Civ: {self.owner.civilisation}, Coordinates: {self.tile.coords}, Goods: {self.goods}."

    def get_city_goods_income(self):
        return self.calculate_goods()

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

        if self.buildings["Free Market"]:
            for _ in self.area:
                self.granary.add_gold(3)

        if self.buildings["Mines"]:
            self.granary.add_stone(20)

    def collect_from_city(self):
        """
        This method should be called to collect all materials from this city granary to player's master granary
        """
        self.owner.granary.insert_from(self.granary)

    def calculate_goods(self):
        goods = self.calculate_goods_no_city(self.area)

        if self.buildings["Free Market"]:
            for _ in self.area:
                goods["gold"] += 3

        if self.buildings["Mines"]:
            goods["stone"] += 20
        return goods

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

    def collect_units(self):
        # print("Begin collecting units.")
        # print(self.unit_request)
        self.days_left_to_building_completion -= 1
        if self.unit_request is not None and self.days_left_to_building_completion <= 0:
            request = self.unit_request
            tile = self.pick_tile_to_build_at()
            if tile is not None:
                from game_screens.combat.garrison import Garrison
                from game_screens.units import Settler
                if request['type'] == 'Settler':
                    unit = Settler(tile, self.owner)
                else:
                    unit = Garrison(tile, self.owner, request['type'], request['count'])
                tile.occupant = unit
                print(f"Unit {str(unit)} finished recruiting.")
                self.unit_request = None
                return unit
            else:
                print(f"No space left near the city for a new unit.")
        return None

    def collect_building(self):
        if self.building_request is None:
            return

        self.days_left_to_building_building_completion -= 1  # maybe this should be moved down?
        if self.days_left_to_building_building_completion <= 0:
            self.buildings[self.building_request] = True

            self.building_request = None
            self.days_left_to_building_building_completion = 0
            self.goods = self.calculate_goods()
            print("Build!")
            print(self.buildings)

    def pick_tile_to_build_at(self):
        for t in self.area:
            if not t.occupied() and t.type != 0 and t.type != 3 and t.coords != self.tile.coords:
                return t
        return None

    def set_area(self, area: list):
        self.area = area
        self.goods = self.calculate_goods()

    def get_random_city_visualization_path(self):
        chosen = random.choice(os.listdir(os.getcwd() + "/resources/images/" + f"{self.owner.short_civ}"))
        return "resources/images/" + f"{self.owner.short_civ}/" + chosen
