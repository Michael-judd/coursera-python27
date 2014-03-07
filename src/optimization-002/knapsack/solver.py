#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def get_best_estimate(items_sorted, capacity, selections):
    value = 0
    weight = 0
    contributions = [0] * len(items_sorted)
    for i in items_sorted:
        if i.index < len(selections) and selections[i.index] == 0: continue
        if weight + i.weight > capacity:
            contributions[i.index] = ((capacity - weight) * 1.0) / i.weight
            value += i.value * contributions[i.index] 
            break
        value += i.value
        weight += i.weight
        contributions[i.index] = 1
        
    return value, contributions

class Node():
    best_value = 0
    best_selections = []
    items = []
    capacity = 0
    items_sorted = []
    
    def __init__(self, value, room, selections, previous_estimate, previous_contributions):
        self.value = value
        self.room = room
        if previous_estimate != -1:
            self.estimate, self.contributions = previous_estimate, previous_contributions
        else:
            self.estimate, self.contributions = get_best_estimate(Node.items_sorted, Node.capacity, selections)
        self.selections = selections
        
    def get_left_child(self):
        index = len(self.selections)
        item = Node.items[index]
        return Node(self.value + item.value, self.room - item.weight, self.selections + [1], self.estimate, self.contributions)
    
    def get_right_child(self):
        index = len(self.selections)
        item = Node.items[index]
        return Node(self.value, self.room, self.selections + [0], -1, None)
    
    def is_leaf(self):
        return len(self.selections) == len(Node.items)
    
    def __repr__(self):
        return "\n".join(["",str(self.value), str(self.room), str(self.estimate), str(self.selections), str(self.contributions), str(Node.best_selections), str(Node.best_value)])

def branch_and_bound(item_count, capacity, items):
    Node.items = items
    Node.capacity = capacity
    Node.items_sorted = sorted(items, key = lambda i: i.density, reverse = True)
    
    root = Node(0, capacity, [], -1, None)
    stack = [root.get_right_child(), root.get_left_child()]
    while stack:
        node = stack.pop()
        if node.room < 0 or node.estimate < Node.best_value: continue
        
        if node.value == node.estimate and node.value > Node.best_value:
            Node.best_value = node.value
            Node.best_selections = node.selections
            node = None
            continue
        
        if not node.is_leaf():
            stack.append(node.get_right_child())
            stack.append(node.get_left_child())
        
        node = None
    
    if len(Node.best_selections) < len(items):
        items.extend([0] * (len(items) - len(Node.best_selections)))
    
    output_data = str(Node.best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, Node.best_selections))
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

