import itertools
import math
import numpy

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def compute_solution(permutation, original_cities):
    edges = list(pairwise(itertools.chain(permutation, [permutation[0]])))

    length = sum(map(lambda (src, dst): distance(original_cities[src],
                                                 original_cities[dst]), edges))

    return (length, edges)


def distance((x1, y1), (x2, y2)):
    return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.5)


def decode_solution(dist2):
    """Return the permutation associated to the elastic."""

    neuron_city_pair = []

    for i in xrange(dist2.shape[0]):
        city = dist2.min(axis=1).argmin()
        neuron = dist2[city].argmin()

        dist2[city] = numpy.inf
        dist2[:,neuron] = numpy.inf

        neuron_city_pair.append((neuron, city))

    neuron_city_pair.sort(key=lambda x: x[0])
    return map(lambda x: x[1], neuron_city_pair)
