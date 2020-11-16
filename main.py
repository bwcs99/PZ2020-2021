from random import randrange
from game_screens import Game

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

if __name__ == "__main__":
    # uruchom ekrany startowe i niech one zrobia swoje w kwestiach serwera
    # niech zwracaja macierz mapy
    world_map = [[randrange(0, 4) for _ in range(40)] for _ in range(25)]
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, world_map)
    window.run()
