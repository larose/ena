DEFAULT = { 'alpha':                  0.2,
            'beta':                   2.0,
            'init_k':                 0.2,
            'epsilon':               0.02,
            'k_alpha':               0.99,
            'k_update_period':         25, # unit: number of iterations
            'max_num_iter':         10000,
            'num_neurons_factor':     2.5,
            'radius':                 0.1 }

class Parameters:
    def __init__(self, **kwargs):
        self._param = {}

        for param, value in DEFAULT.items():
            self._param[param] = value

        for param, value in kwargs.items():
            if param in self._param and value is not None:
                self._param[param] = value

    def __getitem__(self, param):
        return self._param[param]

    def all(self):
        return self._param
