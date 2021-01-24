import arcade

from .granary import Granary


class Player:
    def __init__(self, nickname, civ, color):
        self.nick = nickname
        self.civilisation = civ
        self.adjective_dic = {"The Great Northern": "northern", "Kaediredameria": "kaedir", "Mixtec": "mixtec",
                              "Kintsugi": "kintsugese"}
        self.short_civ = self.adjective_dic[self.civilisation]

        self.color = eval(f"arcade.color.{str.upper(color)}")

        self.units = arcade.SpriteList()
        self.cities = arcade.SpriteList()
        self.borders = []

        self.granary = Granary(1000, 500, 300, 1000)  # start money, enough to buy everything, for testing
        self.daily_income = {'gold': 0, 'wood': 0, 'stone': 0, 'food': 0}

    def __str__(self):
        return f"({self.nick}, {self.civilisation}, {self.color})"

    def collect_from_cities(self):
        for city in self.cities:
            city.gather_materials()  # may show some warning, don't worry brother
            city.collect_from_city()  # it changes self.granary
            city.collect_building()  # collect_building changes count down, it builds building in city after completion

    def calculate_daily_income(self):
        daily_income = {'gold': 0, 'wood': 0, 'stone': 0, 'food': 0}
        for city in self.cities:
            one_city = city.get_city_goods_income()
            for key in daily_income:
                if key in one_city:
                    daily_income[key] = daily_income[key] + one_city[key]
                else:
                    pass

        print(daily_income)
        self.daily_income = daily_income

    def deploy_units(self):
        units_done = []
        for city in self.cities:
            unit = city.collect_units()
            if unit is not None:
                self.units.append(unit)
                units_done.append(unit)
        return units_done
