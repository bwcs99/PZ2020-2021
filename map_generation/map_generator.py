from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
import random


# rgb(0, 64, 128) woda
# rgb(128, 128, 128) gory
# rgb(16, 128, 64) wzgorza
# rgb(112, 169, 0) rowniny


def noise(nx, ny, gen):
    """ Generate noise value at (nx, ny) using generator gen, tweaked to return a value from (0, 1) """
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def elevation(nx, ny, gen):
    """ Overlap different noise functions to create a height map at (nx, ny) """
    freq1 = 10
    freq2 = 20
    freq3 = 40
    e = 1 * noise(freq1 * nx, freq1 * ny, gen) + 0.5 * noise(freq2 * nx, freq2 * ny, gen) \
        + 0.25 * noise(freq3 * nx, freq3 * ny, gen)
    return e


def biome(val, params):
    """ Quantize value val into ranges specified by params """
    # print(val)
    if val < params[1]:  # woda
        return 0
    if val < params[2]:  # rowniny
        return 1
    if val < params[3]:  # wzgorza
        return 2
    return 3  # gory


def generate_map(width, height, params):
    """ Generate map using given parameters: \n
    params[0] - seed, \n
    params[1] - water quantizer\n
    params[2] - land quantizer \n
    params[3] - hills quantizer \n
    --> Quantizers work in range [1, 30]\n
    --> point (0,0) is top left corner
    """
    seed = params[0]
    gen = OpenSimplex(seed=seed)  # get noise generator
    world_map = []
    random.seed(seed)
    exponent = random.uniform(3, 5)
    for x in range(width):
        world_map.append([0] * height)
        for y in range(height):
            nx = x / width - 0.5
            ny = y / height - 0.5
            e = elevation(nx, ny, gen)
            val = pow(e, exponent) * 10
            world_map[x][y] = biome(val, params)
    return world_map


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


world_map = generate_map(300, 300, [1,8,28,6])

get_map_overview(world_map)


