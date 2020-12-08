import unittest

from start_screens import img_gen as img
from . import map_generator as gen
from . import spread_players as s


class MapCase(unittest.TestCase):
    def test_map_overview_accuracy(self):
        """ Test if image of map overview properly represents generated map matrix. """
        params = [10000, 5, 10, 15]
        height = 100
        width = 200
        world_map = gen.generate_map(height=height, width=width, params=params)
        image = img.get_map_overview(world_map)
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                color = tuple(img.get_color(world_map[x][y]))
                self.assertEqual(pixels[x, y], color)

    def test_spreading_players(self):
        """ Test if players are properly spread across. """
        params = [3, 4, 11, 20]
        w = gen.generate_map(height=50, width=80, params=params)
        coords = s.spread_across_the_map(w, 4)
        for c in coords:
            x = c[0]
            y = c[1]
            self.assertNotEqual(w[x][y], 0)
            self.assertNotEqual(w[x][y], 3)  # uncomment the block to see an overview
        #     w[x][y] = 4
        # image = img.get_map_overview(w)
        # image2 = img.get_resized_map_overview(image, 781, 521)
        # image2.show()


if __name__ == '__main__':
    unittest.main()
