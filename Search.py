#!/usr/bin/env python3
import sys
from collections import deque
import queue

print("arg list: " + str(sys.argv))

# global variables
input_file = sys.argv[1]
start_node = int(sys.argv[2])
end_node = int(sys.argv[3])
search_type = sys.argv[4] # 'BFS' or 'DFS', or 'UCS'

nodes = {}    # dictionary storing the neighbors of each node
# TODO: consider renaming to 'discovered'
added = {}    # (dictionary) of already explored/expanded nodes
              # nodes are paired with the id of their parents
weights = {}  # dictionary of the weights of the edges between connected nodes
q = deque([]) # FIFO queue



# read data from input file and store it
def readFile(fileName):
    f = open(fileName, "r") # open file for reading

    for line in f:
        ##print(line)
        # split each line (by space character) into array of ints
        vals = list(map(int, line.split()))

        source = vals[0] # the edge's source node
        dest = vals[1]   # the edge's destination node
        weight = vals[2] # the edge's weight

        # store the weight of this edge
        weights[edgeName(source, dest)] = weight
        writeNode(source, dest) # remember that these nodes are connected
    f.close()


# get the weight betweeen two nodes
# @param id1, id2: int IDs of the nodes
def getWeight(id1, id2):
    return weights[edgeName(id1, id2)]


# returns the name of the edge containing the two nodes
# @param id1, id2: int IDs of the nodes
def edgeName(id1, id2):
    # make sure id1 < id2
    if id1 > id2:
        temp = id1
        id1 = id2
        id2 = temp
    return str(id1) + "-" + str(id2)


# TODO: nodes should be added to in numerical order to your expansion data structure.
#       can we assume the data is provided in numerical order?
# @param id1, id2: int IDs of the node and its neighbor
def writeNode(id1, id2):
    if id1 not in nodes:
        nodes[id1] = []
    nodes[id1].append(id2)

    if id2 not in nodes:
        nodes[id2] = []
    nodes[id2].append(id1)


def BFS(id):

    ##else:
        ##print("at node " + str(id))

    for n in nodes[int(id)]:
        # check that the neighbors haven't been already added
        if n not in added:
            ##print(" -adding " + str(n))
            q.append(int(n)) # add the connected nodes to the queue
            added[n] = id # indicate that this node is already in the queue

    # when q not empty
    if q:
        ##print(added)
        BFS(int(q.popleft()))

    else:
    #if id == end_node:
        ##print "*** at goal node: " + str(id)
        res = []
        cur = end_node

        while cur != None:
            res = [cur] + res
            cur = added[cur]

        ##print("SOLUTION:")
        print(res)


def UCS():

    if not q.empty():
        cur = q.get()
        id = int(cur[1])
        weight = int(cur[0])
        print(str(cur[0]) + ", " + str(id))

        for n in nodes[int(id)]:
            if n not in added:
                print(" -adding " + str(n))
                total_weight = weight + getWeight(id, n)
                q.put((total_weight, n)) # add the connected nodes to the queue
                added[n] = id # indicate that this node is already in the queue
                              # remeber the ID of its parent

        UCS()
    else:
        res = []
        cur = end_node

        while cur != None:
            res = [cur] + res
            cur = added[cur]

        print("SOLUTION:")
        print(res)

readFile(input_file)

##print("\nnodes:")
##print(nodes)
##print("\nweights:")
##print(weights)

if search_type == "BFS":
    q.append(start_node)
    added[start_node] = None

    BFS(int(q.popleft()))

if search_type == "UCS":
    ##print("performing UCS")
    q = queue.PriorityQueue()
    q.put((0, start_node)) # insert this tuple (priority, id) into the priority queue
    added[start_node] = None
    UCS()


##print("\n")
