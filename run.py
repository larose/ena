import elastic_net
import instance
import math
import optparse
import os
import os.path
import parameters
import pprint
import string
import solution
import sys
import time


def main():
    options, args = parse_arguments()

    print "- - - - - - - - -"
    print "- Initilization -"
    print "- - - - - - - - -"
    print
    
    print "Reading '%s'..." % args[0],
    inst = instance.make_instance(args[0])
    print "OK"
    
    output_dir = make_output_dir(inst.name, options.output_dir)
    evolution_period = options.evolution
    if evolution_period >= 0:
        print "Creating directory '%s'..." % output_dir,
        os.makedirs(output_dir)
        print "OK"
        
    param = parameters.Parameters(**vars(options))
    elastic = elastic_net.ElasticNet(inst.cities, param)
    
    zfill_length = int(math.log10(param['max_num_iter']) + 1)
    rjust_length = zfill_length + 5

    print
    print
    print "- - - - - - -"
    print "- Algorithm -"
    print "- - - - - - -"
    print
    print "Stop criteria:"
    print "   max number of iterations: %d" % param['max_num_iter']
    print "   worst distance          : %f" % param['epsilon']
    print
    print "Parameters"
    pprint.pprint(param.all())
    print
    print "Starting algorithm..."
    print
    print string.rjust("Iteration", rjust_length), "     Worst distance"

    while elastic.iteration():
        num_iter = elastic.num_iter - 1

        if (num_iter % 100 == 0):
            print string.rjust(str(num_iter), rjust_length) + "     ",
            print elastic._worst_dist

        if evolution_period > 0 and (num_iter % evolution_period == 0):
            draw_elastic(num_iter, inst.cities, elastic.neurons, zfill_length,
                         output_dir)

    if evolution_period >= 0:
        draw_elastic(elastic.num_iter - 1, inst.cities,
                     elastic.neurons, zfill_length, output_dir)


    permutation    = solution.decode_solution(elastic.dist2)
    (value, edges) = solution.compute_solution(permutation,
                                               inst.original_cities)

    if evolution_period >= 0:
        import draw
        figure = draw.Figure()
        figure.add_cities(inst.cities)
        figure.add_solution(inst.cities, edges)
        figure.savefig(os.path.join(output_dir, "solution.png"))

    print
    print
    print "- - - - - -"
    print "- Summary -"
    print "- - - - - -"
    print

    if evolution_period >= 0:
        print "Output directory    : %s" % output_dir
    print "Number of iterations: %d" % elastic.num_iter
    print "Worst distance      : %f" % elastic.worst_dist
    print "Tour length         : %d" % value
    print "Solution            : %s" % permutation


def draw_elastic(num_iter, cities, neurons, zfill_length, output_dir):
    import draw
    figure = draw.Figure()
    figure.add_cities(cities)
    figure.add_neurons(neurons)
    filename = "elastic-" + \
        string.zfill(num_iter, zfill_length) + ".png"
    figure.savefig(os.path.join(output_dir, filename))
    
            
def make_output_dir(name, prefix):
    if prefix is None:
        prefix = os.getcwd()

    output_dir = os.path.join(
        prefix,
        name + "-" + time.strftime("%Y-%m-%d@%H-%M-%S"))

    return output_dir
    
            
def parse_arguments():
    parser = optparse.OptionParser("Usage: %prog [options] filename")

    parser.add_option("-a", "--alpha",
                      type = float,
                      dest = "alpha")
        
    parser.add_option("-b", "--beta",
                      type = float,
                      dest = "beta")
    
    parser.add_option("-k", "--init_k",
                      type = float,
                      dest = "init_k")

    parser.add_option("-e", "--epsilon",
                      type = float,
                      dest = "epsilon")

    parser.add_option("-c", "--k_alpha",
                      type = float,
                      dest = "k_alpha")

    parser.add_option("-i", "--k_update_period",
                      type = int,
                      dest = "k_update_period")

    parser.add_option("-m", "--max_num_iter",
                      type = int,
                      dest = "max_num_iter")

    parser.add_option("-f", "--num_neurons_factor",
                      type = float,
                      dest = "numNeuronsFactor")

    parser.add_option("-r", "--radius",
                      type = float,
                      dest = "radius")

    
    parser.add_option("-v", "--evolution",
                      type = int,
                      dest = "evolution",
                      default = 0,
                      help = """Save the elastic to a file every
                      `evolution` iterations. Save only at the end if
                      evolution = 0. Save nothing if evolution < 0.""")


    parser.add_option("-o", "--output_dir",
                      type = "string",
                      dest = "output_dir")
    

    options, args = parser.parse_args()

    if len(args) != 1:
        print "Argument error. Execute with --help."
        sys.exit(-1)

    return options, args


if __name__ == '__main__':
    main()
