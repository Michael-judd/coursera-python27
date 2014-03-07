#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def get_best_estimate(items_sorted, capacity, selections):
    value = 0
    weight = 0
    for idx in xrange(len(items_sorted)):
        if idx < len(selections) and selections[idx] == 0: continue
        i = items_sorted[idx]
        if weight + i.weight > capacity:
            value += i.value * (((capacity - weight) * 1.0) / i.weight) 
            break
        value += i.value
        weight += i.weight

    return value

def get_an_estimate(items_sorted, capacity, selections):
    return sum(0 if idx < len(selections) and selections[idx] == 0 else items_sorted[idx].value for idx in xrange(len(items_sorted)))

class Node():
    best_value = 0
    best_selections = []
    capacity = 0
    items_sorted = []
    
    def __init__(self, value, room, selections, previous_estimate):
        self.value = value
        self.room = room
        self.estimate = previous_estimate if previous_estimate != -1 else get_best_estimate(Node.items_sorted, Node.capacity, selections)
        self.selections = selections
        self.index = len(self.selections)
        
    def get_left_child(self):
        item = Node.items_sorted[self.index]
        return Node(self.value + item.value, self.room - item.weight, self.selections + [1], self.estimate)
    
    def get_right_child(self):
        item = Node.items_sorted[self.index]
        return Node(self.value, self.room, self.selections + [0], -1)
    
    def is_leaf(self):
        return self.index == len(Node.items_sorted)
    
def branch_and_bound(item_count, capacity, items):
    Node.best_value = 0
    Node.best_selections = []
    Node.capacity = capacity
    Node.items_sorted = sorted(items, key = lambda i: i.density, reverse = True)
    
    root = Node(0, capacity, [], -1)
    stack = [root.get_right_child(), root.get_left_child()]
    while stack:
        node = max(stack, key = lambda i: i.value)
        stack.remove(node)
        
        if node.room < 0 or node.estimate < Node.best_value: continue
        
        if node.is_leaf() and node.value > Node.best_value:
            Node.best_value = node.value
            Node.best_selections = node.selections
            continue
        
        if not node.is_leaf():
            stack.append(node.get_left_child())
            stack.append(node.get_right_child())
    
    selections = [0] * len(items)
    for idx in xrange(len(Node.best_selections)):
        if Node.best_selections[idx] == 1: selections[Node.items_sorted[idx].index] = 1
    
    output_data = str(Node.best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, selections))
    return output_data


def dynamic_programming(item_count, capacity, items):
    items.insert(0, Item(0, 0, 0, 0))
    val_mat = [[0] * (item_count + 1) for _ in xrange(capacity + 1)]
    for i, c in ((a, b) for a in xrange(1, item_count + 1) for b in xrange(1, capacity + 1)):
        val_mat[c][i] = max(val_mat[c][i - 1],  0 if items[i].weight > c else val_mat[c - items[i].weight][i - 1] + items[i].value)

    taken = [0] * item_count
    cap = capacity
    for i in xrange(item_count, 0, -1):
        if val_mat[cap][i] > val_mat[cap][i - 1]:
            taken[i-1] = 1
            cap -= items[i].weight
    
    # prepare the solution in the specified output format
    output_data = str(val_mat[capacity][item_count]) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    item_count, capacity = map(int, lines[0].split())

    items = []
    for i in range(1, item_count+1):
        v, w = map(int, lines[i].split())
        items.append(Item(i-1, v, w, (v * 1.0) / w))

    
    #return dynamic_programming(item_count, capacity, items)
    return branch_and_bound(item_count, capacity, items)


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

