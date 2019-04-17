import pdb


leftbank = []
rightbank = []

class Node:
    def __init__(self,val, child = []):     # Node("",[Node(4),Node(5)])
        self.val = val
        self.child = child

class Graph:
    def __init__(self, val, children):
        self.state = Node(val, children)
        

    def add_successor_nodes(self,nodes):
        for node in nodes:
            self.state.child.append(Node(node))

x  = Graph(3,[Node(5,[Node(3)])])       # Syntax similar to functional programming
# alternatively can use a dict mapping for denoting relationships on a graph
pdb.set_trace()
def graph_search (problem, fringe):
    closed = []
    fringe = []     # Is kinda like the fifo queue
