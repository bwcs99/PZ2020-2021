import unittest
from . import map_generator as gen


class MapCase(unittest.TestCase):
    def test_map_overview_accuracy(self):
        """ Test if image of map overview properly represents generated map matrix """
        params = [10000, 5, 10, 15]
        height = 100
        width = 200
        world_map = gen.generate_map(height=height, width=width, params=params)
        image = gen.get_map_overview(world_map)
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                color = tuple(gen.get_color(world_map[x][y]))
                self.assertEqual(pixels[x, y], color)


if __name__ == '__main__':
    unittest.main()
