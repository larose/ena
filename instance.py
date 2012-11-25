import numpy
import os

class Instance:
    def __init__(self, name, cities):
        self._name = name
        self._original_cities = numpy.array(cities, dtype=float)
        self._normalize_cities()

    def _normalize_cities(self):
        min = self._original_cities.min(axis=0)
        max = self._original_cities.max(axis=0)
        self._cities = (self._original_cities - min) / (max - min)

    def _get_cities(self):
        return self._cities
    cities = property(fget=_get_cities)

    def _get_original_cities(self):
        return self._original_cities
    original_cities = property(fget=_get_original_cities)

    def _get_name(self):
        return self._name
    name = property(fget=_get_name)

def make_instance(filename):
    file = open(filename)
    cities = []
    
    for line in file:
        x, y = line.strip().split()
        cities.append((int(x), int(y)))
        
    return Instance(os.path.basename(filename), cities)


