import errno
import math
import optparse
import os
import pprint
import sys
import tempfile

import elastic_net
import instance
import parameters
import solution

def main():
    options, args = parse_arguments()

    print_initialization()

    inst = make_instance(args[0])

    output_dir       = options.output_dir or tempfile.mkdtemp(prefix="ena-")
    evolution_period = options.evolution
    param            = parameters.Parameters(**vars(options))
    elastic          = elastic_net.ElasticNet(inst.cities, param)
    zfill_length     = int(math.log10(param['max_num_iter']) + 1)
    rjust_length     = zfill_length + 5

    draw_elastic = make_draw_elastic(inst.cities, zfill_length, output_dir)

    make_output_directory(output_dir)

    print_algorithm()
    print_stop_criteria(param['max_num_iter'], param['epsilon'])
    print_parameters(param)
    print_starting_algorithm(rjust_length)
    
    run_algorithm(inst, elastic, evolution_period, rjust_length, draw_elastic)

    if evolution_period >= 0:
        draw_elastic(elastic.num_iter - 1, elastic.neurons)

    permutation    = solution.decode_solution(elastic.dist2)
    (value, edges) = solution.compute_solution(permutation,
                                               inst.original_cities)

    if evolution_period > 0:
        import draw
        draw.draw_final_solution(inst.cities, edges,
                                 os.path.join(output_dir, "solution.png"))

    print_summary(output_dir, elastic, value, permutation)
    write_solution(output_dir, permutation, value)

    
def make_instance(filename):
    print("Reading '%s'..." % filename, end=' ')
    inst = instance.make_instance(filename)
    print("OK")
    return inst

def make_draw_elastic(cities, zfill_length, output_dir):
    def draw_elastic(num_iter, neurons):
        import draw
        filename = "elastic-" + str(num_iter).zfill(zfill_length) + ".png"
        draw.draw_intermediate_solution(cities, neurons, 
                                        os.path.join(output_dir, filename))
        
    return draw_elastic

def make_output_directory(output_dir):
    print("Creating output directory: '%s'..." % output_dir, end=' ')
    try:
        os.makedirs(output_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    print("OK")
            
def parse_arguments():
    parser = optparse.OptionParser("Usage: %prog filename [options]")

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
        print("Argument error. Execute with --help.")
        sys.exit(-1)

    return options, args

def print_algorithm():
    print()
    print()
    print("- - - - - - -")
    print("- Algorithm -")
    print("- - - - - - -")
    print()

def print_initialization():
    print("- - - - - - - - -")
    print("- Initilization -")
    print("- - - - - - - - -")
    print()

def print_parameters(param):
    print("Parameters")
    pprint.pprint(param.all())
    print()

def print_starting_algorithm(rjust_length):
    print("Starting algorithm...")
    print()
    print("Iteration".rjust(rjust_length), "     Worst distance")

def print_stop_criteria(max_num_iter, epsilon):
    print("Stop criteria:")
    print("   max number of iterations >= %d" % max_num_iter)
    print("   or")
    print("   worst distance           >= %f" % epsilon)
    print()

def print_summary(output_dir, elastic, value, permutation):
    print()
    print()
    print("- - - - - -")
    print("- Summary -")
    print("- - - - - -")
    print()
    print("Number of iterations: %d" % elastic.num_iter)
    print("Worst distance      : %f" % elastic.worst_dist)
    print("Tour length         : %d" % value)
    print("Solution            : %s" % permutation)
    print("Output directory    : %s" % output_dir)

def run_algorithm(inst, elastic, evolution_period, rjust_length, draw_elastic):
    while elastic.iteration():
        num_iter = elastic.num_iter - 1
        
        if (num_iter % 100 == 0):
            print(str(num_iter).rjust(rjust_length) + "     ", end=' ')
            print(elastic._worst_dist)

        if evolution_period > 0 and (num_iter % evolution_period == 0):
            draw_elastic(num_iter, elastic.neurons)

def write_solution(output_dir, permutation, value):
    solution_file = open(os.path.join(output_dir, 'solution'), 'w')
    solution_file.write(' '.join(map(str,permutation)) + '\n')

    length_file = open(os.path.join(output_dir, 'solution.length'), 'w')
    length_file.write(str(value) + '\n')

if __name__ == '__main__':
    main()
