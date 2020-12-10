import os
import random

import arcade

from .granary import Granary


class City(arcade.sprite.Sprite):
    def __init__(self, unit, area):
        super().__init__(":resources:images/tiles/brickGrey.png")
        self.name = self.get_random_city_name()
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

    def __str__(self):
        return f"City_name: {self.name}, Owner: {self.owner.nick}, Civ: {self.owner.civilisation}, Coordinates: {self.tile.coords}, Goods: {self.goods}."

    def gather_materials(self):
        """
        Gathering materials works as follows: checking all tiles in self.area and adding appropriate values to granary.
        TODO optimization of consts

        """
        for tile in self.area:
            if tile.type == 0:
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
        goods = {'gold': 0, 'wood': 0, 'stone': 0, 'food': 0}
        for tile in self.area:
            if tile.type == 0:
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

    def get_random_city_visualization_path(self):
        chosen = random.choice(os.listdir("resources/images/" + f"{self.owner.short_civ}"))
        return "resources/images/" + f"{self.owner.short_civ}/" + chosen
