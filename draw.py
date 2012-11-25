import itertools
import numpy
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

def draw_intermediate_solution(cities, neurons, filename):
    figure = plt.figure()
    figure.gca().axison = False
    _draw_cities(figure, cities)
    _draw_elastic(figure, neurons)
    figure.savefig(filename)

def draw_final_solution(cities, edges, filename):
    figure = plt.figure()
    figure.gca().axison = False
    _draw_cities(figure, cities)
    _draw_edges(figure, cities, edges)
    
    figure.savefig(filename)

def _draw_cities(figure, cities):
    figure.gca().scatter(cities[:,0], cities[:,1], s=15, color='black')

def _draw_edges(figure, cities, edges):
    edge_collection = LineCollection(cities[numpy.array(edges)], 
                                     edgecolor='blue')
    figure.gca().add_collection(edge_collection)
    
def _draw_elastic(figure, neurons):
    edges = list(_pairwise(itertools.chain(range(len(neurons)), [0])))
    edge_collection = LineCollection(neurons[edges], edgecolor='green')
    figure.gca().add_collection(edge_collection)
    figure.gca().scatter(neurons[:,0], neurons[:,1], s=3, color='green')

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
