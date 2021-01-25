from server_utils.client import Client
from game_screens.granary import Granary
from game_screens.game_logic import GameLogic
from game_screens.player import Player
import unittest

PORT = 65001
HOST = '127.0.0.1'


class TestNewLogic(unittest.TestCase):
    player1 = Player("a", "The Great Northern", "red")
    player2 = Player("b", "Kaediredameria", "blue")
    p1_granary = Granary(100, 200, 300, 400)
    p2_granary = Granary(500, 500, 500, 500)
    client = Client()

    def test_update_allies_list(self):
        GameLogic.update_allies_list(self, self.player1, self.player2, True)
        p1_allies = [self.player2.nick]
        p2_allies = [self.player1.nick]
        self.assertEqual(self.player1.allies, p1_allies)
        self.assertEqual(self.player2.allies, p2_allies)
        GameLogic.update_allies_list(self, self.player1, self.player2, False)
        p1_allies = []
        p2_allies = []
        self.assertEqual(self.player1.allies, p1_allies)
        self.assertEqual(self.player2.allies, p2_allies)

    def test_update_enemies_list(self):
        GameLogic.update_enemies_list(self, self.player1, self.player2, True)
        p1_enemies = [self.player2.nick]
        p2_enemies = [self.player1.nick]
        self.assertEqual(self.player1.enemies, p1_enemies)
        self.assertEqual(self.player2.enemies, p2_enemies)
        GameLogic.update_enemies_list(self, self.player1, self.player2, False)
        p1_enemies = []
        p2_enemies = []
        self.assertEqual(self.player1.enemies, p1_enemies)
        self.assertEqual(self.player2.enemies, p2_enemies)

    def test_handle_buying_process(self):
        GameLogic.handle_buying_process(self, self.player1.nick, self.p1_granary, self.p2_granary, (False, "food"), 50, 1)
        self.assertEqual(self.p1_granary.food, 401)
        self.assertEqual(self.p1_granary.gold, 50)
        self.assertEqual(self.p2_granary.food, 499)
        self.assertEqual(self.p2_granary.gold, 550)

    def test_handle_selling_process(self):
        GameLogic.handle_selling_process(self, self.p1_granary, self.p2_granary, "food", 100, 8)
        self.assertEqual(self.p1_granary.food, 393)
        self.assertEqual(self.p1_granary.gold, 150)
        self.assertEqual(self.p2_granary.food, 507)
        self.assertEqual(self.p2_granary.gold, 450)

    def test_display_to_others(self):
        msg_queue = [f'BUY:ala:edyta:(False, "wood"):70:7:False',
                    f'SELL:edyta:jaroslaw:(False, "food"):80:2:False',
                    f'EAL_INFO:radoslaw:jaroslaw',
                    f'DCL_WAR_INFO:ala:monika',
                    f'ALC_INFO:ala:edyta',
                    f'GUP_INFO:radoslaw:jaroslaw',
                    f'TRC_INFO:ala:monika',
                    f'B_INFO:ala:monika:(6,7)']

        answer = [f'Alliance between radoslaw and jaroslaw ended',
                  f'ala has declared war to monika',
                  f'ala and edyta are allies',
                  f'radoslaw gave up. War between radoslaw'
                  f'and jaroslaw ended',
                  f'ala sent truce request to monika. War between'
                  f'them is ended',
                  f'ala has bought (6, 7) city from monika'
                  ]

        test_output = self.client.display_message_to_others(msg_queue)
        self.assertEqual(test_output, answer)

    def test_display_message(self):
        msg_queue = [f'ALLIANCE:ala:ola:False', f'ALLIANCE_ANSWER:ala:ola:True',
                     f'BUY:olga:monika:(False, "food"):80:4:False',
                     f'SELL:olga:monika:stone:40:4:False']
        answer = [f'ala wants alliance with you', f'You and ola are allies',
                  f'olga wants to buy food from you. Qunatity: 4.'
                            f'Price: 80',
                  f'olga wants to sell you stone. Qunatity: 4.Price: 40']

        test_output = self.client.display_message_queue(msg_queue)
        self.assertEqual(answer, test_output)


if __name__ == '__main__':
    unittest.main()

