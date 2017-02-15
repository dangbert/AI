#!/usr/bin/env python3
import sys
from collections import deque
import queue
sys.path.append("/pqdict")
from pqdict import pqdict # http://pqdict.readthedocs.io/en/latest/pqdict.html#pqdict-class

#print("arg list: " + str(sys.argv))

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
stack = []    # list used as a stack


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


# @param id1, id2: int IDs of the node and its neighbor
def writeNode(id1, id2):
    if id1 not in nodes:
        nodes[id1] = []
    nodes[id1].append(id2)

    # this is a directional graph, not bidirectional!
    #if id2 not in nodes:
    #    nodes[id2] = []
    #nodes[id2].append(id1)


def BFS(id):
    if id in nodes:
        for n in nodes[int(id)]:
            # check that the neighbors haven't been already added
            if n not in added:
                q.append(int(n)) # add the connected nodes to the queue
                added[n] = id    # indicate that this node is already in the queue
                                 # and store its parent

    # when q not empty
    if q:
        BFS(int(q.popleft()))

    else:
        res = []
        cur = end_node

        while cur != None:
            res = [cur] + res
            cur = added[cur]

        print(res)

def DFS(id):
    #print(" DFS, ID = " + str(id))
    if id in nodes:
        for n in nodes[int(id)]:
            # check that the neighbors haven't been already added
            if n not in added:
                stack.append(int(n)) # add the connected nodes to the queue
                added[n] = id    # indicate that this node is already in the queue
    #else:
    #    print(" ... not in nodes")

    if stack:
        DFS(int(stack.pop()))

    else:
        res = []
        cur = end_node

        while cur != None:
            res = [cur] + res
            cur = added[cur]

        print(res)


def UCS():
    pq = pqdict({start_node: 0})

    visited = {}
    parent = {start_node: None}

    while True:
        try:
            cur_cost = pq[pq.top()]
            cur = pq.pop() # ID of the node that we're currently visiting
            #print("\npopped " + str(cur) + ", " + str(cur_cost))

            for n in nodes[int(cur)]: # neighbors of current node
                if n not in visited:
                    #print(" -at neighbor " + str(n))
                    # calculate the distance to n
                    n_cost = cur_cost + getWeight(cur, n)
                    #print("    cost to " + str(n) + ": " + str(n_cost))

                    if n in pq:
                        #print("    already in pq")
                        if n_cost < pq[n]:
                            pq[n] = n_cost # update priority
                            parent[n] = cur # update parent
                            #print("    *updated priority")
                        #else:

                            #print("    " + str(n) + " has lower (existing) cost " + str(pq[n]))
                    else:
                        # add to priority queue
                        #print("    ADDING to queue")
                        pq[n] = n_cost
                        parent[n] = cur

            visited[cur] = None
            if cur == end_node:
                break


            #pq['a'] = 99 # updates the priority of 'a'

        except KeyError:
            break

    # queue is now empty
    res = []
    temp = end_node

    while temp != None:
        res = [temp] + res
        temp = parent[temp]
    print(res)



readFile(input_file)
# sort nodes by increasing ID
for n in nodes:
    nodes[n] = sorted(nodes[n])


if search_type == "BFS":
    q.append(start_node)
    added[start_node] = None
    BFS(int(q.popleft()))

if search_type == "DFS":
    stack.append(start_node)
    added[start_node] = None
    DFS(int(stack.pop()))

if search_type == "UCS":
    UCS()


##print("\n")
