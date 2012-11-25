import math
import numpy

class ElasticNet:
    def __init__(self, cities, param):
        self._cities = cities
        self._param = param
        self._num_iter = 0
        self._k = self._param['init_k']
        self._num_neurons = int(self._param['num_neurons_factor'] \
                                    * self._cities.shape[0])
        self._init_neurons()

    def iteration(self):
        """
        Perform one iteration of the algorithm.

        Return True if the algorithm has finished, False otherwise.
        """
        
        self._num_iter += 1
        self._update_k()
        self._update_weights()
        self._update_neurons()

        return not self._stop_criteria()

    def _get_dist2(self):
        return self._dist2
    dist2 = property(fget=_get_dist2)
    
    def _get_neurons(self):
        return self._neurons
    neurons = property(fget=_get_neurons)

    def _get_num_iter(self):
        return self._num_iter
    num_iter = property(fget=_get_num_iter)

    def _get_worst_dist(self):
        return self._worst_dist
    worst_dist = property(fget=_get_worst_dist)
    
    def _dist_force(self):
        """
        Compute the force that minimize the distance between the
        cities and the neurons.
        """
        
        return numpy.array(
            [numpy.dot(self._weights[:,i],
                       self._delta[:,i]) for i in range(self._num_neurons)])

    def _init_neurons(self):
        """
        Initialize the neurons in a circle at the center of the
        cities.
        """
        
        theta = numpy.linspace(0, 2 * math.pi, self._num_neurons, False)
        centroid = self._cities.mean(axis=0)
        
        self._neurons = numpy.vstack((numpy.cos(theta), numpy.sin(theta)))
        self._neurons *= self._param['radius']
        self._neurons += centroid[:,numpy.newaxis]
        self._neurons = self._neurons.transpose()

    def _length_force(self):
        """Compute the force that minimize the length of the elastic."""
        
        return numpy.concatenate((
            [self._neurons[1] - 2 * self._neurons[0] 
             + self._neurons[self._num_neurons - 1]],
            
            [(self._neurons[i+1]
              - 2 * self._neurons[i]
              + self._neurons[i-1])
             for i in range(1, self._num_neurons - 1)],
            
            [self._neurons[0]
             - 2 * self._neurons[self._num_neurons - 1]
             + self._neurons[self._num_neurons - 2]]))

    def _stop_criteria(self):
        """Return True if the algorithm has finished, False otherwise."""
        
        return self._worst_dist < self._param['epsilon'] \
            or self._num_iter  >= self._param['max_num_iter']

    def _update_k(self):
        if (self._num_iter % self._param['k_update_period']) == 0:
            self._k = max(0.01, self._param['k_alpha'] * self._k)
        
    def _update_neurons(self):
        dist_force = self._dist_force()
        length_force = self._length_force()

        self._neurons += self._param['alpha'] * dist_force \
            + self._param['beta'] * self._k * length_force
        
    def _update_weights(self):
        """Compute w_ij, i = 1, 2, ..., |Cities|; j = 1, 2, ...., |Neurons|"""
        
        self._delta = self._cities[:,numpy.newaxis] - self._neurons

        # At this point
        # self._delta[i,j] == (delta_x, delta_y) between city i and neuron j

        self._dist2 = (self._delta ** 2).sum(axis=2)

        # At this point
        # self._dist2[i,j] == square of the distance between city i and neuron j

        self._worst_dist = numpy.sqrt(self._dist2.min(axis=1).max())

        self._weights = numpy.exp(-self._dist2 / (2 * (self._k ** 2)))

        # At this point
        # self._weights[i,j] == unnormalized weight associated to city
        # i and neuron j

        self._weights /= self._weights.sum(axis=1)[:,numpy.newaxis]

        # At this point
        # self._weights[i,j] == normalized weight associated to city i
        # and neuron j
        

        


