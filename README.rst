Elastic Net Algorithm
=====================

This is an implementation of the elastic net algorithm proposed by
Durbin and Willshaw [1] to solve the Travelling Salesman Problem.

The elastic net algorithm is an iterative procedure where M points,
with M larger than the number of citiqes N, are lying on a circular
ring or "rubber band" originally located at the center of the
cities. The rubber band is gradually elongated until it passes
sufficiently near each city to define a tour. During that process two
forces apply: one for minimizing the length of the ring, and the other
one for minimizing the distance between the cities and the points on
the ring. These forces are gradually adjusted as the procedure
evolves. [2]

Examples
--------

Show help message. ::

    python run.py --help

Solve `tsp22` instance. ::

    python run.py instances/tsp_22

Export the elastic every 100 iterations. ::

    python run.py instances/tsp_22 --evolution 100


Optimal Values
--------------

+----------+--------------+
| Instance | Optimal Value|
+==========+==============+
|tsp22     | 278          |
+----------+--------------+
| tsp30    | 420          +
+----------+--------------+
| tsp51    | 426          +
+----------+--------------+
| tsp76    | 538          +
+----------+--------------+
| tsp100   | 21294        +
+----------+--------------+

Dependencies
------------



+-------------+-----------+---------------------------------+
| Library     | Version   | Note                            |
+=============+===========+=================================+
|matplotlib   | 1.0.1+    | Optional. Only to export to PNG.|
+-------------+-----------+---------------------------------+
|numpy        | 1.6.1+    |                                 |
+-------------+-----------+---------------------------------+


Author
------

Mathieu Larose <mathieu.larose.ml@gmail.com>


References
----------

[1] `Durbin, R. and Willshaw, D. An Analogue Approach to the Travelling Salesman Problem using an Elastic Net Method. Nature 326, 689-691, 1987.`_ 

[2] `Potvin, J-Y. The Traveling Salesman Problem: A Neural Network Perspective, 1993.`_

.. _`Durbin, R. and Willshaw, D. An Analogue Approach to the Travelling Salesman Problem using an Elastic Net Method. Nature 326, 689-691, 1987.`: http://www2.mrc-lmb.cam.ac.uk/archive/papers/CP49-76.pdf

.. _`Potvin, J-Y. The Traveling Salesman Problem: A Neural Network Perspective, 1993.`: http://ce.sharif.ir/courses/84-85/2/ce667/resources/root/Seminar_no_7/paper_potvin_nn_tsp.pdf


