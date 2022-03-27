import random
from functools import reduce


def multiple_values_in_list(values):
    return reduce(lambda x, y: x * y, values)


def get_random_struct_values(vertices):
    return [bool(random.randint(0, 1)) for v in range(vertices)]
