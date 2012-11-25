import itertools
import math
import numpy

def compute_solution(permutation, original_cities):
    edges = list(_pairwise(itertools.chain(permutation, [permutation[0]])))

    length = sum([distance(original_cities[src_dst[0]],
                           original_cities[src_dst[1]]) for src_dst in edges])

    return (length, edges)

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.5)

def decode_solution(dist2):
    """Return the permutation associated to the elastic."""

    neuron_city_pair = []

    for i in range(dist2.shape[0]):
        city = dist2.min(axis=1).argmin()
        neuron = dist2[city].argmin()

        dist2[city] = numpy.inf
        dist2[:,neuron] = numpy.inf

        neuron_city_pair.append((neuron, city))

    neuron_city_pair.sort(key=lambda x: x[0])
    return [x[1] for x in neuron_city_pair]

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
