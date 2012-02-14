import itertools
import numpy
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


class Figure(object):
    def __init__(self):
        plt.clf()
        plt.gca().axison = False

    def add_cities(self, cities):
        plt.scatter(cities[:,0],
                    cities[:,1],
                    s=15,
                    color='black')

    def add_neurons(self, neurons):
        edges = list(pairwise(itertools.chain(xrange(len(neurons)), [0])))
        edge_collection = LineCollection(neurons[edges], edgecolor='green')
        plt.gca().add_collection(edge_collection)
        
        plt.scatter(neurons[:,0],
                    neurons[:,1],
                    s=3,
                    color='green')

    def add_solution(self, cities, edges):
        edge_collection = LineCollection(cities[numpy.array(edges)],
                                         edgecolor='blue')
        plt.gca().add_collection(edge_collection)

    def savefig(self, filename):
        plt.savefig(filename)
