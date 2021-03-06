import pdb
import sys
import queue
import copy
import itertools

# Graph Definition
class Node:
    def __init__(self,val, child = [], leftbank = [], rightbank = [], priority = 0, parent = None):     # Node("",[Node(4),Node(5)])
        self.val = val
        self.child = child
        self.leftbank = leftbank      # C, W, B
        self.rightbank = rightbank    # C, W, B
        self.priority = priority
        self.parent = parent
    
    def __lt__(self, other):
        return (self.priority > other.priority)

class Graph:
    def __init__(self, val, children, leftbank = [], rightbank = []):
        self.state = Node(val, children, leftbank, rightbank)
        

    def add_successor_nodes(self,nodes):
        for node in nodes:
            self.state.child.append(Node(node))

def main():
    # Reading Files for Start State
    start_file = open(sys.argv[1], "r")
    x = start_file.readline()
    leftstart = [int(i.strip()) for i in x.split(',')]
    x = start_file.readline()
    rightstart = [int(i.strip()) for i in x.split(',')]

    # Reading Files for Goal State
    goal_file = open(sys.argv[2], "r")
    x = goal_file.readline()
    leftgoal = [int(i.strip()) for i in x.split(',')]
    x = goal_file.readline()
    rightgoal = [int(i.strip()) for i in x.split(',')] 

    mode = sys.argv[3]
    file_name = sys.argv[4]
    outputfile = open(file_name, "w")

    inp = make_graph(leftstart, rightstart)
    exp_out = make_graph(leftgoal, rightgoal)

    if mode == "bfs":
        result, numNodesExpanded = bfs_graph_search(inp.state,exp_out.state)
        print("Number of nodes expanded is: ", numNodesExpanded)
        print("Solution has ", result.val, " paths")
        print_path(result, outputfile)
    elif mode == "dfs":
        result, numNodesExpanded = dfs_graph_search(inp.state,exp_out.state)
        print("Number of nodes expanded is: ", numNodesExpanded)
        print("Solution has ", result.val, " paths")
        print_path(result, outputfile)
    elif mode == "iddfs":
        x = iddfs_graph_search(inp.state,exp_out.state)
        x = flatten(x)
        print("Number of nodes expanded is: ", x[1])
        print("Solution has ", x[0].val, " paths")
        print_path(x[0], outputfile)
    elif mode == "astar":
        result, numNodesExpanded = a_star_search(inp.state,exp_out.state)
        print("Number of nodes expanded is: ", numNodesExpanded)
        print("Solution has ", result.val, " steps")
        print_path(result, outputfile)

    # x = iddfs_graph_search(inp.state,exp_out.state)
    # print_path(x, outputfile)
    # xx = flatten(x)
    # pdb.set_trace()
    # print(x.leftbank)
    # print(x.rightbank)
    # print(y)
    # pdb.set_trace()

def make_graph(left_bank, right_bank):
    return (Graph(0, [], left_bank, right_bank))

# input  = Graph(3,[Node(5,[Node(3)])])       # Syntax similar to functional programming
# alternatively can use a dict mapping for denoting relationships on a graph

def succ(state, max_chick, max_wolf):
    initial_left = copy.deepcopy(state.leftbank)
    left_chick = initial_left[0]
    left_wolf = initial_left[1]
    left_boat = initial_left[2]

    initial_right = copy.deepcopy(state.rightbank)
    right_chick = initial_right[0]
    right_wolf = initial_right[1]
    right_boat = initial_right[2]

    # Temp arrays for successors banks
    succleftbank = copy.deepcopy(initial_left)
    succrightbank = copy.deepcopy(initial_right)

    # Temp array for set of successor states
    succset = []
    # pdb.set_trace()
    # Where is the boat?
    if (left_boat == 1):
        if ((left_wolf <= left_chick - 1 or left_wolf == 0 or left_chick - 1 == 0) and (right_wolf <= right_chick + 1 or right_wolf == 0 or right_chick + 1 == 0)):     # Checking constraint
            # Put one chicken in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succleftbank[0] -= 1
            succrightbank[0] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((left_wolf <= left_chick - 2 or left_wolf == 0 or left_chick - 2 == 0) and (right_wolf <= right_chick + 2 or right_wolf == 0 or right_chick + 2 == 0)): 
            # Put two chickens in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succleftbank[0] -= 2
            succrightbank[0] += 2
            succleftbank[2] = 0
            succrightbank[2] = 1
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((left_wolf - 1 <= left_chick or left_wolf - 1 == 0 or left_chick == 0) and (right_wolf + 1 <= right_chick or right_wolf + 1 == 0 or right_chick == 0)): 
            # Put one wolf in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succleftbank[1] -= 1
            succrightbank[1] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((left_wolf - 1 <= left_chick - 1 or left_wolf - 1 == 0 or left_chick - 1 == 0) and (right_wolf + 1 <= right_chick + 1 or right_wolf + 1 == 0 or right_chick + 1 == 0)):
            # Put one wolf and one chicken in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succleftbank[0] -= 1
            succrightbank[0] += 1
            succleftbank[1] -= 1
            succrightbank[1] += 1
            succleftbank[2] = 0
            succrightbank[2] = 1
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((left_wolf - 2 <= left_chick or left_wolf - 2 == 0 or left_chick == 0) and (right_wolf + 2 <= right_chick or right_wolf + 2 == 0 or right_chick == 0)):
            # Put two wolves in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succleftbank[1] -= 2
            succrightbank[1] += 2
            succleftbank[2] = 0
            succrightbank[2] = 1
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
    elif (right_boat == 1):
        if ((right_wolf <= right_chick - 1 or right_wolf == 0 or right_chick - 1 == 0) and (left_wolf <= left_chick + 1 or left_wolf == 0 or left_chick + 1 == 0)):     # Checking constraint
            # Put one chicken in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succrightbank[0] -= 1
            succleftbank[0] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((right_wolf <= right_chick - 2 or right_wolf == 0 or right_chick - 2 == 0) and (left_wolf <= left_chick + 2 or left_wolf == 0 or left_chick + 2 == 0)): 
            # Put two chickens in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succrightbank[0] -= 2
            succleftbank[0] += 2
            succleftbank[2] = 1
            succrightbank[2] = 0
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((right_wolf - 1 <= right_chick or right_wolf - 1 == 0 or right_chick == 0) and (left_wolf + 1 <= left_chick or left_wolf + 1 == 0 or left_chick == 0)): 
            # Put one wolf in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succrightbank[1] -= 1
            succleftbank[1] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((right_wolf - 1 <= right_chick - 1 or right_wolf - 1 == 0 or right_chick - 1 == 0) and (left_wolf + 1 <= left_chick + 1 or left_wolf + 1 == 0 or left_chick + 1 == 0)):
            # Put one wolf and one chicken in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succrightbank[0] -= 1
            succleftbank[0] += 1
            succrightbank[1] -= 1
            succleftbank[1] += 1
            succleftbank[2] = 1
            succrightbank[2] = 0
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
        if ((right_wolf - 2 <= right_chick or right_wolf - 2 == 0 or right_chick == 0) and (left_wolf + 2 <= left_chick or left_wolf + 2 == 0 or left_chick == 0)):
            # Put two wolves in the boat
            succleftbank = copy.deepcopy(initial_left)
            succrightbank = copy.deepcopy(initial_right)
            succrightbank[1] -= 2
            succleftbank[1] += 2
            succleftbank[2] = 1
            succrightbank[2] = 0
            flag = 1
            for i in range(3):
                if(succleftbank[i] < 0 or succrightbank[i] < 0):
                    flag = 0
            if(succleftbank[0] + succrightbank[0] > max_chick):
                flag = 0
            if(succleftbank[1] + succrightbank[1] > max_wolf):
                flag = 0
            if(flag == 1):
                # Create state(node) and add to set of returned states
                succset.append(Node(state.val + 1, [], succleftbank, succrightbank, 0, state))
    return succset


def bfs_graph_search (state, goal):
    max_chick = state.rightbank[0]
    max_wolf = state.rightbank[1]
    closed = []
    fringe = queue.Queue()     # Is kinda like the fifo queue (Queue)
    fringe.put(state)          # Enqueue state
    visited = set()            # Creating dictionary(hash map) for visited nodes
    numNodesExpanded = 0
    while fringe:
        cur = fringe.get()
        if (cur.leftbank == goal.leftbank and cur.rightbank == goal.rightbank):
            return cur, numNodesExpanded                          
        if (str(cur.leftbank + cur.rightbank)) not in visited:              # Using hash set
            visited.add(str(cur.leftbank + cur.rightbank))                # Adding to visited (modify to use unique key instead of depth or use hashset)
            temp = succ(cur, max_chick, max_wolf)                # Expanding
            numNodesExpanded += 1
            # pdb.set_trace()
            # print("hello")
            for _node in temp:
                fringe.put(_node)           # Add states to fringe
                cur.child.append(_node)     # Add children to cur node in graph

def dfs_graph_search (state, goal):
    max_chick = state.rightbank[0]
    max_wolf = state.rightbank[1]
    closed = []
    fringe = queue.LifoQueue()     # A LiFo queue (stack)
    fringe.put(state)          # Enqueue state
    visited = set()            # Creating dictionary(hash map) for visited nodes
    numNodesExpanded = 0
    while fringe:
        cur = fringe.get()
        if (cur.leftbank == goal.leftbank and cur.rightbank == goal.rightbank):
            return cur, numNodesExpanded                          
        if (str(cur.leftbank + cur.rightbank)) not in visited:              # Using hash set
            visited.add(str(cur.leftbank + cur.rightbank))                # Adding to visited (modify to use unique key instead of depth or use hashset)
            temp = succ(cur, max_chick, max_wolf)                # Expanding
            numNodesExpanded += 1
            # pdb.set_trace()
            # print("hello")
            for _node in temp:
                fringe.put(_node)           # Add states to fringe
                cur.child.append(_node)     # Add children to cur node in graph

def iddfs_graph_search(state, goal):
    numNodesExpanded = 0
    max_chick = state.rightbank[0]
    max_wolf = state.rightbank[1]
    for depth in itertools.count():
        result = dls(state, goal, numNodesExpanded, depth, max_chick, max_wolf)
        if result != "notFound":
            return result, numNodesExpanded

def dls(state, goal, numNodesExpanded, depth, max_chick, max_wolf):
    visited = set()
    return recursive_dls(state, goal, numNodesExpanded, depth, max_chick, max_wolf, visited)

def recursive_dls(state, goal, numNodesExpanded, depth, max_chick, max_wolf, visited):
    if (state.leftbank == goal.leftbank and state.rightbank == goal.rightbank):
        return state, numNodesExpanded
    elif depth == 0:
        return "notFound"
    else:
        cutoff_occurred = False
        cur = state
        if (str(cur.leftbank + cur.rightbank)) not in visited:              # Using hash set
            visited.add(str(cur.leftbank + cur.rightbank))                # Adding to visited (modify to use unique key instead of depth or use hashset)
            temp = succ(cur, max_chick, max_wolf)                # Expanding
            numNodesExpanded += 1
        
            for successor in temp:
                result = recursive_dls(successor, goal, numNodesExpanded, depth - 1, max_chick, max_wolf, visited)
                if result == "notFound":
                    cutoff_occurred = True
                elif result:
                    return result, numNodesExpanded
            if cutoff_occurred:
                return "notFound"
            else:
                return False
        return "notFound"

            
# https://www.reddit.com/r/learnpython/comments/5yxgd4/flatten_a_nested_list_using_recursion_simplify/
def flatten(sequence: tuple) -> tuple:
    result = []
    stack = [sequence]
    while stack:
        current = stack.pop(-1)
        if isinstance(current, tuple):
            stack.extend(current)
        else:
            result.append(current)
    result.reverse()
    return result   

def heuristic(node):
    if (node.leftbank[0] + node.leftbank[1] > node.rightbank[0] + node.rightbank[1]):
        return 0.75

    else:
        return 0.25


def a_star_search(state, goal):
    max_chick = state.rightbank[0]
    max_wolf = state.rightbank[1]
    if (state.leftbank == goal.leftbank and state.rightbank == goal.rightbank):
        return state
    fringe = queue.PriorityQueue()
    fringe.put(state)
    visited = set()
    numNodesExpanded = 0
    while fringe:
        cur = fringe.get()
        try:
            if (len(cur) == 2):
                cur = cur[1]
        except:
            pass
        if (cur.leftbank == goal.leftbank and cur.rightbank == goal.rightbank):
            return cur, numNodesExpanded
        new_states = succ(cur, max_chick, max_wolf)
        numNodesExpanded += 1
        if (str(cur.leftbank + cur.rightbank)) not in visited:              # Using hash set
            visited.add(str(cur.leftbank + cur.rightbank))                # Adding to visited (modify to use unique key instead of depth or use hashset)
            temp = succ(cur, max_chick, max_wolf)                # Expanding
            numNodesExpanded += 1
            for _node in new_states:
                _node.priority = (_node.val + heuristic(_node))
                fringe.put((_node.priority, _node))
        



def print_path (node, outputfile):
    if (node.parent == None):
        outputfile.write(str(node.leftbank) + " " + str(node.rightbank) + ", ")
        print(node.leftbank, node.rightbank, end = ", ")
    else:
        print_path(node.parent,outputfile)
        outputfile.write(str(node.leftbank) + " " + str(node.rightbank) + ", ")
        print(node.leftbank, node.rightbank, end = ", ")
 
main()