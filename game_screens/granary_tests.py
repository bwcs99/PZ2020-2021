import unittest

from granary import Granary


class GranaryTests(unittest.TestCase):
    def test_emptying_granary(self):
        granary = Granary(10, 13, 15, 232)
        granary.empty_granary()
        self.assertEqual(granary.gold, 0)
        self.assertEqual(granary.wood, 0)
        self.assertEqual(granary.stone, 0)
        self.assertEqual(granary.food, 0)

    def test_inserting_from(self):
        granary1 = Granary(10, 20, 30, 40)
        granary2 = Granary(100, 200, 300, 400)
        granary1.insert_from(granary2)
        self.assertEqual(granary1.gold, 110)
        self.assertEqual(granary1.wood, 220)
        self.assertEqual(granary1.stone, 330)
        self.assertEqual(granary1.food, 440)

    def test_Salomon(self):
        granary = Granary(0, 0, 32, 0)
        self.assertFalse(granary.try_to_sub_stone(40))


if __name__ == '__main__':
    unittest.main()
