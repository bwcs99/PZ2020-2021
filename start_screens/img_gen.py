from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
import random

def get_color(tile):
    """ Return RGB value tied to tile type """
    if tile == 0:  # woda
        return [0, 64, 128]
    if tile == 1:  # rowniny
        return [112, 169, 0]
    if tile == 2:  # wzgorza
        return [16, 128, 64]
    if tile == 3:  # gory
        return [128, 128, 128]
    return [0, 0, 0]


def get_map_overview(world_map):
    """ Return image object of generated world map"""
    x = len(world_map)
    y = len(world_map[0])
    arr = np.zeros([x, y, 3], dtype=np.uint8)
    for i in range(x):
        for j in range(y):
            arr[i, j] = get_color(world_map[i][j])
    img = Image.fromarray(arr)
    """ Pillow swaps height with width, so we need to tweak the image to actually represent the map"""
    img = img.rotate(270, expand=1).transpose(Image.FLIP_LEFT_RIGHT)  # rotate clockwise and do mirror flip
    img.save('testrgb.png')
    return img

