#!/usr/bin/env python
import sys

print("arg list: " + str(sys.argv))

# global variables
input_file = sys.argv[1]
start_node = sys.argv[2]
end_node = sys.argv[3]
search_type = sys.argv[4] # 'BFS' or 'DFS', or 'UCS'

nodes = {} # dictionary
weights = {}

# read data from input file and store it
def readFile(fileName):
    f = open(fileName, "r") # open file for reading

    for line in f:
        # split each line (by space character) into array of ints
        vals = map(int, line.split())

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


# @param id1, id2: int IDs of the node and its neighbor
def writeNode(id1, id2):
    if id1 not in nodes:
        nodes[id1] = []
    nodes[id1].append(id2)

    if id2 not in nodes:
        nodes[id2] = []
    nodes[id2].append(id1)

# need list of already explored/expanded nodes (hash table?)
# need way to retrieve the neighbors of a node when "building" the search tree

readFile(input_file)

print("\nnodes:")
print(nodes)
print("\nweights:")
print(weights)
