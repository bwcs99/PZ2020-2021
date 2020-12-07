import arcade


class City(arcade.sprite.Sprite):
    def __init__(self, unit):
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
