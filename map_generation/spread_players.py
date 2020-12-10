import random
from math import sqrt


def spread_across_the_map(world_map, number_of_players, seed=None):
    """ Returns a list of coordinates for the players to start the game. """
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()
    players_set = []
    width = len(world_map)
    height = len(world_map[0])
    idle_counter = 0
    while number_of_players > 0:
        idle_counter += 1
        if idle_counter > 1000:
            raise Exception("Too many iterations to spread players")
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        if world_map[x][y] == 0 or world_map[x][y] == 3:
            continue  # try again
        if players_are_in_proximity(players_set, x, y):
            continue  # try again
        players_set.append([x, y])
        number_of_players -= 1
    return players_set


def players_are_in_proximity(players_set, x, y):
    min_range = 15
    for c in players_set:
        x1 = c[0]
        y1 = c[1]
        if sqrt((x1 - x) ** 2 + (y1 - y) ** 2) <= min_range:
            return True
    return False
