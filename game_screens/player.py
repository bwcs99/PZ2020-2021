import arcade

from .granary import Granary

class Player:
    def __init__(self, nickname, civ, color):
        self.nick = nickname
        self.civilisation = civ
        self.adjective_dic = {"The Great Northern": "northern", "Kaediredameria": "kaediredameria", "Mixtec": "mixtec",
                              "Kintsugi": "kintsugi"}
        self.short_civ = self.adjective_dic[self.civilisation]

        self.color = eval(f"arcade.color.{str.upper(color)}")

        self.units = arcade.SpriteList()
        self.cities = arcade.SpriteList()
        self.borders = []

        self.granary = Granary()

    def __str__(self):
        return f"({self.nick}, {self.civilisation}, {self.color})"

    def collect_from_cities(self):
        for city in self.cities:
            print(city)
            city.gather_materials()  # may show some warning, don't worry brother
            city.collect_from_city()  # it's ok
            print(self.granary)

