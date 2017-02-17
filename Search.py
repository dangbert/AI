#!/usr/bin/env python3
import sys
from collections import deque
import queue
sys.path.append("/pqdict") # only way to include the library on Mimir
from pqdict import pqdict # http://pqdict.readthedocs.io/en/latest/pqdict.html#pqdict-class


# class for searching a directed graph
class GraphSearch:
    # constructor
    def __init__(self, input_file):
        self._nodes = {}    # dictionary storing the neighbors each node can access
        self._added = {}    # (dictionary) of already discovered nodes
                            # TODO: make added a set called discovered
                            # TODO: use parent instead to remember parents
                            # nodes are paired with the id of their parents
        self._parent = {}

        self._weights = {}  # dictionary of the weights of the edges between connected nodes
        self._q = deque([]) # FIFO queue
        self._stack = []    # list used as a stack

        self._readFile(input_file)


    # read data from the input file about the graph
    def _readFile(self, input_file):
        f = open(input_file, "r") # open file for reading

        for line in f:
            # split each line (by space character) into array of ints
            vals = list(map(int, line.split()))

            source = vals[0] # the edge's source node
            dest = vals[1]   # the edge's destination node
            weight = vals[2] # the edge's weight

            # store the weight of this edge
            self._weights[self._edgeName(source, dest)] = weight
            self._writeNode(source, dest) # remember that these nodes are connected
        f.close()

        # sort node neighbors by increasing ID
        for n in self._nodes:
            self._nodes[n] = sorted(self._nodes[n])


    # TODO: reset everything after doing a graph search and printing results
    def BFS(self, start_node, end_node):
        self._q.append(start_node)
        self._parent[start_node] = None
        self._added[start_node] = 1

        while self._q:
            id = int(self._q.popleft())
            if id in self._nodes:
                for n in self._nodes[int(id)]:
                    # check that the neighbors haven't been already added
                    if n not in self._added:
                        self._added[n] = 1     # indicate that this node is already in the queue
                        self._q.append(int(n)) # add the connected nodes to the queue
                        self._parent[n] = id # update parent
                                         # and store its parent
        self._printResults(self._parent, end_node)   # print results


    def DFS(self, start_node, end_node):
        self._parent = {start_node: None}
        self._stack.append(start_node)
        self._added[start_node] = 1
        found = False

        while self._stack and not found:                         # stack not empty
            id = int(self._stack.pop())

            if id in self._nodes:
                for n in reversed(self._nodes[int(id)]):
                    # check that the neighbors haven't been already added
                    if n not in self._added:
                        # TODO: consider using set instead of dictionary (for added)
                        self._added[n] = 1          # indicate that this node is already in the queue
                        self._stack.append(int(n))  # add the connected nodes to the queue
                        self._parent[n] = id # update parent
                        if n == end_node:
                            found = True
                            break
        self._printResults(self._parent, end_node)


    def UCS(self, start_node, end_node):
        pq = pqdict({start_node: 0})             # priority queue
        visited = {}
        self._parent = {start_node: None}

        while True:
            try:
                cur_cost = pq[pq.top()]
                cur = int(pq.pop()) # ID of the node that we're currently visiting

                for n in self._nodes[cur]: # neighbors of current node
                    if n not in visited:
                        # calculate the cost to reach node n
                        n_cost = cur_cost + self._getWeight(cur, n)

                        if n in pq:
                            if n_cost < pq[n]:
                                # cheaper route to node discovered
                                pq[n] = n_cost   # update priority
                                self._parent[n] = cur  # update parent
                        else:
                            pq[n] = n_cost       # add to priority queue
                            self._parent[n] = cur      # remember how we reached n

                visited[cur] = None
                if cur == end_node:
                    break

            except KeyError:
                # priority queue is empty
                break
        self._printResults(self._parent, end_node)


    # prints the final results as an array of node IDs
    # TODO: use self._parent instead after fixing added
    def _printResults(self, parent, end_node):
        res = []               # array of the order to visit the nodes
        temp = end_node

        if end_node in parent:
            while temp != None:
                res = [temp] + res
                temp = parent[temp]
        print(res)


    # get the weight of the edge betweeen two nodes
    def _getWeight(self, id1, id2):
        return self._weights[self._edgeName(id1, id2)]


    # returns the (string) name of the edge containing two nodes
    def _edgeName(self, id1, id2):
        # make sure id1 < id2
        if id1 > id2:
            temp = id1
            id1 = id2
            id2 = temp
        return str(id1) + "-" + str(id2)


    # TODO: rename writeEdge
    # add an edge to the graph pointing from src node to dest node
    def _writeNode(self, src, dest):
        if src not in self._nodes:
            self._nodes[src] = []
        self._nodes[src].append(dest)

        # this is a directional graph, not bidirectional!
        #if dest not in nodes:
        #    nodes[dest] = []
        #nodes[dest].append(src)


# global variables
input_file = sys.argv[1]
start_node = int(sys.argv[2])
end_node = int(sys.argv[3])
search_type = sys.argv[4] # 'BFS' or 'DFS', or 'UCS'


graph = GraphSearch(input_file)

if search_type == "BFS":
    graph.BFS(start_node, end_node)

if search_type == "DFS":
    #parent = {start_node: None}

    #stack.append(start_node)
    #added[start_node] = 1
    #DFS(int(stack.pop()))
    graph.DFS(start_node, end_node)

if search_type == "UCS":
    graph.UCS(start_node, end_node)
