import arcade
from granary import Granary


class City(arcade.sprite.Sprite):
    def __init__(self, unit, surrounding: list):
        super().__init__(":resources:images/tiles/brickGrey.png")
        self.color = unit.color
        self.tile = unit.tile
        self.tile.city = self
        self.area = []
        self.width = self.tile.width
        self.height = self.tile.height
        self.owner = unit.owner
        self.center_x = self.tile.center_x
        self.center_y = self.tile.center_y

        self.surrounding = surrounding
        self.granary = Granary()
        self.gather_materials()  # for tactic usages, when you build city, you get materials right away

    def gather_materials(self):
        for tile in self.surrounding:
            print(tile.color)
            if tile.type == 0:
                self.granary.add_food(10)
            if tile.type == 1:
                self.granary.add_food(5)
                self.granary.add_wood(5)
            if tile.type == 2:
                self.granary.add_food(3)
                self.granary.add_wood(10)
            if tile.type == 3:
                self.granary.add_stone(5)
