#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx
from ortools.constraint_solver import pywrapcp

def solve_it(input_data):
    lines = input_data.split('\n')
    node_count, edge_count = map(int, lines[0].split())
    edges = [map(int, line.split()) for line in lines[1:] if line]
    
    graph = networkx.Graph()
    graph.add_nodes_from([idx for idx in range(node_count)])
    graph.add_edges_from(edges)
    
    max_colours_required = max(graph.degree().values()) + 1

    solver = pywrapcp.Solver('graph-coloring')
    
    degrees = graph.degree()
    node_idx_mapping = {}
    idx = 0
    nodes = []
    for w in sorted(degrees, key = degrees.get, reverse = True):
        node_idx_mapping[w] = idx
        nodes.append(solver.IntVar(0, max_colours_required - 1, 'Node-%i' % w))
        idx += 1

    max_color = solver.Max(nodes).Var() 
    
    for a, b in edges:
        solver.Add(nodes[node_idx_mapping[a]] != nodes[node_idx_mapping[b]])

    for clique in networkx.find_cliques(graph):
        solver.Add(solver.AllDifferent([nodes[node_idx_mapping[idx]] for idx in clique]))

    solver.Add(nodes[0] == 0)

    objective = solver.Minimize(max_color, 1)

    solution = solver.Assignment()
    solution.Add(nodes)
    solution.Add(max_color)
    
    db = solver.Phase(nodes, solver.ASSIGN_CENTER_VALUE, solver.ASSIGN_MIN_VALUE)
    collector = solver.LastSolutionCollector(solution)
    
    limit = solver.TimeLimit(2 * 60 * 1000)
    
    #statsvisitor = solver.StatisticsModelVisitor()
    #solver.Accept(statsvisitor, [collector, objective, limit])
    
    solver.Solve(db, [collector, objective, limit])
    
    reverse_node_idx_mapping = {}
    for k, v in node_idx_mapping.items():
        reverse_node_idx_mapping[v] = k
    
    color_solution = [0] * node_count
    for idx in range(node_count):
        color_solution[reverse_node_idx_mapping[idx]] = str(collector.Value(0, nodes[idx]))
    
    output_data = str(int(collector.Value(0, max_color)) + 1) + ' ' + str(0) + '\n'
    output_data += ' '.join(color_solution)
    
    #print "max_colours_required:", max_colours_required
    #print "failures:", solver.Failures()
    #print "branches:", solver.Branches()
    #print "WallTime:", solver.WallTime()
    
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

