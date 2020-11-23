import random

from opensimplex import OpenSimplex


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
    """ Generate map using given parameters:
    params[0] - seed,
    params[1] - water quantizer
    params[2] - land quantizer
    params[3] - hills quantizer
    --> Ideally params[1] < params[2] < params[3], everything above params[3] is considered mountains
    --> Quantizers work best in range [1, 30]
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


