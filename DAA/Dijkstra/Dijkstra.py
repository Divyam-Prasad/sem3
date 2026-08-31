# It is algorithm that finds the lowest cost path from a source(starting node) to a target(goal node).

# It uses a simple technique to select the next node or candidate to visit.

# Here, I will implement a simple code for Dijkstra's algorithm.
# 
#  

# Node class to make a node 

# A -- B,C
# B -- C
# C -- D
# D -- E

import math 
class Node:
    def __init__(self, data):
        self.data = data
        self.neighbours = []
        # self.cost = math.inf

    def add_neighbours(self, neighbours):
        self.neighbours = neighbours


def Dijkstra(source, goal, visited):
    temp_neighbours = []
    for item in source.neighbours:
        temp_neighbours.append(item)
    for item in temp_neighbours:
        if item.cost >  + : 
             