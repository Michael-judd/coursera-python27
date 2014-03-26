#!/usr/bin/python
# -*- coding: utf-8 -*-

from ortools.constraint_solver import pywrapcp

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    node_count, edge_count = map(int, lines[0].split())
    edges = [(map(int, line.split())) for line in lines[1:] if line]

    solver = pywrapcp.Solver('graph-coloring')
    nodes = [solver.IntVar(0, node_count - 1, 'Node-%i' % i) for i in range(node_count)]
    
    for a, b in edges:
        solver.Add(nodes[a] != nodes[b])
    
    solution = solver.Assignment()
    solution.Add(nodes)
    
    #collector = solver.AllSolutionCollector(solution)
    collector = solver.FirstSolutionCollector(solution)
    
    solver.Solve(solver.Phase(nodes, solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE), [collector])
    
    qval = [collector.Value(0, nodes[i]) for i in range(node_count)]
    
    output_data = str(len(set(qval))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, qval))

    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

