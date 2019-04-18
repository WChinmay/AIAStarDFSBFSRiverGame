import pdb
import sys
import queue

# Graph Definition
class Node:
    def __init__(self,val, child = [], leftbank = [], rightbank = []):     # Node("",[Node(4),Node(5)])
        self.val = val
        self.child = child
        self.leftbank = leftbank      # C, W, B
        self.rightbank = rightbank    # C, W, B

class Graph:
    def __init__(self, val, children, leftbank = [], rightbank = []):
        self.state = Node(val, children, leftbank, rightbank)
        

    def add_successor_nodes(self,nodes):
        for node in nodes:
            self.state.child.append(Node(node))

# Reading Files for Start State
sys.argv = [sys.argv[0], 'start1.txt']
start_file = open(sys.argv[1], "r")
x = start_file.readline()
leftstart = []
leftstart.append(x[0])
leftstart.append(x[2])
leftstart.append(x[4])
x = start_file.readline()
rightstart = []
rightstart.append(x[0])
rightstart.append(x[2])
rightstart.append(x[4])

# Reading Files for Goal State
sys.argv = [sys.argv[0], 'goal1.txt']
goal_file = open(sys.argv[1], "r")
x = goal_file.readline()
leftgoal = []
leftgoal.append(x[0])
leftgoal.append(x[2])
leftgoal.append(x[4])
x = goal_file.readline()
rightgoal = []  
rightgoal.append(x[0])
rightgoal.append(x[2])
rightgoal.append(x[4])

def make_graph(left_bank, right_bank):
    return (Graph(0, [], left_bank, right_bank))



# input  = Graph(3,[Node(5,[Node(3)])])       # Syntax similar to functional programming
# alternatively can use a dict mapping for denoting relationships on a graph

def succ(state):
    initial_left = state.leftbank
    left_chick = initial_left[0]
    left_wolf = initial_left[1]
    left_boat = initial_left[2]

    initial_right = state.rightbank
    right_chick = initial_right[0]
    right_wolf = initial_right[1]
    right_boat = initial_right[2]

    # Temp arrays for successors banks
    succleftbank = initial_left
    succrightbank = initial_right

    # Temp array for set of successor states
    succset = []
    pdb.set_trace()
    # Where is the boat?
    if (left_boat == 1):
        if ((left_wolf <= left_chick - 1) and (right_wolf <= right_chick + 1)):     # Checking constraint
            # Put one chicken in the boat
            succleftbank = initial_left
            succrightbank = initial_right
            succleftbank[0] -= 1
            succrightbank[0] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((left_wolf <= left_chick - 2) and (right_wolf <= right_chick + 2)): 
            # Put two chickens in the boat
            succleftbank = initial_left
            succrightbank = initial_right
            succleftbank[0] -= 2
            succrightbank[0] += 2
            succleftbank[2] = 0
            succrightbank[2] = 1
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((left_wolf - 1 <= left_chick) and (right_wolf + 1 <= right_chick)): 
            # Put one wolf in the boat
            succleftbank = initial_left
            succrightbank = initial_right
            succleftbank[1] -= 1
            succrightbank[1] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((left_wolf - 1 <= left_chick - 1) and (right_wolf + 1 <= right_chick + 1)):
            # Put one wolf and one chicken in the boat
            succleftbank = initial_left
            succrightbank = initial_right
            succleftbank[0] -= 1
            succrightbank[0] += 1
            succleftbank[1] -= 1
            succrightbank[1] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((left_wolf - 2 <= left_chick) and (right_wolf + 2 <= right_chick)):
            # Put two wolves in the boat
            succleftbank = initial_left
            succrightbank = initial_right
            succleftbank[1] -= 2
            succrightbank[1] += 2
            succleftbank[2] = 0
            succrightbank[2] = 1
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
    elif (right_boat == 1):
        if ((right_wolf <= right_chick - 1) and (left_wolf <= left_chick + 1)):     # Checking constraint
            # Put one chicken in the boat
            succrightbank = initial_right
            succleftbank = initial_left
            succrightbank[0] -= 1
            succleftbank[0] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((right_wolf <= right_chick - 2) and (left_wolf <= left_chick + 2)): 
            # Put two chickens in the boat
            succrightbank = initial_right
            succleftbank = initial_left
            succrightbank[0] -= 2
            succleftbank[0] += 2
            succleftbank[2] = 1
            succrightbank[2] = 0
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((right_wolf - 1 <= right_chick) and (left_wolf + 1 <= left_chick)): 
            # Put one wolf in the boat
            succrightbank = initial_right
            succleftbank = initial_left
            succrightbank[1] -= 1
            succleftbank[1] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((right_wolf - 1 <= right_chick - 1) and (left_wolf + 1 <= left_chick + 1)):
            # Put one wolf and one chicken in the boat
            succrightbank = initial_right
            succleftbank = initial_left
            succrightbank[0] -= 1
            succleftbank[0] += 1
            succrightbank[1] -= 1
            succleftbank[1] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
        if ((right_wolf - 2 <= right_chick) and (left_wolf + 2 <= left_chick)):
            # Put two wolves in the boat
            succrightbank = initial_right
            succleftbank = initial_left
            succrightbank[1] -= 2
            succleftbank[1] += 2
            succleftbank[2] = 1
            succrightbank[2] = 0
            # Create state(node) and add to set of returned states
            succset.append(Node(state.val + 1, [], succleftbank, succrightbank))
    return succset


def bfs_graph_search (state, goal):
    closed = []
    fringe = queue.Queue()     # Is kinda like the fifo queue (Queue)
    fringe.put(state)          # Enqueue state
    visited = set()            # Creating dictionary(hash map) for visited nodes
    numNodesExpanded = 0
    while fringe:
        cur = fringe.get()
        if (cur.leftbank == goal.leftbank and cur.rightbank == goal.rightbank):
            return cur, numNodesExpanded                          
        if cur not in visited:              # Using hash set
            visited.add(cur)                # Adding to visited (modify to use unique key instead of depth or use hashset)
            print(len(cur.child))
            temp = succ(cur)                # Expanding
            print(len(cur.child),"kdvgnklsndl")
            numNodesExpanded += 1
            # pdb.set_trace()
            print("hello")
            for _node in temp:
                fringe.put(_node)           # Add states to fringe
                cur.child.append(_node)     # Add children to cur node in graph
                print(len(cur.child))
            print("if loop")
        print(cur.val)
        print("outside")
        pdb.set_trace() 

def dfs_graph_search (state, goal):
    closed = []
    fringe = queue.LifoQueue()     # A LiFo queue in Python (Stack)
    fringe.put(state)          # Enqueue state
    visited = set()            # Creating dictionary(hash map) for visited nodes
    numNodesExpanded = 0
    while fringe:
        cur = fringe.get()
        if (cur.leftbank == goal.leftbank and cur.rightbank == goal.rightbank):
            return cur, numNodesExpanded                          
        if cur not in visited:              # Using hash set
            visited.add(cur)                # Adding to visited (modify to use unique key instead of depth or use hashset)
            temp = succ(cur)                # Expanding
            numNodesExpanded += 1
            for _node in temp:
                fringe.put(_node)           # Add states to fringe
                cur.child.append(_node)     # Add children to cur node in graph





inp = make_graph(leftstart, rightstart)
exp_out = make_graph(rightstart, leftstart)

bfs_graph_search(inp.state,exp_out.state)
pdb.set_trace()

print("")
