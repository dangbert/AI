#!/usr/bin/env python3
import sys
from collections import deque
import queue
sys.path.append("/pqdict")                      # only way to include the library on Mimir
from pqdict import pqdict                       # http://pqdict.readthedocs.io/en/latest/pqdict.html#pqdict-class


# class for searching a directed graph
class GraphSearch:

    # constructor
    def __init__(self, input_file):
        self._nodes = {}                        # dictionary storing the neighbors each node can access
        self._weights = {}                      # dictionary of the weights of the edges between connected nodes
        self._readFile(input_file)


    # read data from the input file about the graph
    def _readFile(self, input_file):
        f = open(input_file, "r")               # open file for reading

        for line in f:
            # split each line (by space character) into array of ints
            vals = list(map(int, line.split()))

            source = vals[0]                    # the edge's source node
            dest = vals[1]                      # the edge's destination node
            weight = vals[2]                    # the edge's weight

            # store the weight of this edge
            self._weights[self._edgeName(source, dest)] = weight
            self._addEdge(source, dest)         # remember that these nodes are connected
        f.close()

        # sort node neighbors by increasing ID
        for n in self._nodes:
            self._nodes[n] = sorted(self._nodes[n])


    # perform breadth first search on the graph
    def BFS(self, start_node, end_node):
        q = deque([start_node])                 # FIFO queue
        parent = {start_node: None}             # dictionary storing the parent (ID) of each traversed node
        discovered = {start_node}               # set of already discovered nodes

        # while queue not empty
        while q:
            id = int(q.popleft())
            if id in self._nodes:
                for n in self._nodes[int(id)]:
                    # check that the neighbors haven't been already discovered
                    if n not in discovered:
                        q.append(int(n))        # add the connected node to the queue
                        parent[n] = id          # update parent
                        discovered.add(n)       # indicate this node has been added to the queue
        self._printResults(parent, end_node)    # print results


    # perform depth first search on the graph
    def DFS(self, start_node, end_node):
        stack = [start_node]                    # list used as a stack
        parent = {start_node: None}             # dictionary storing the parent (ID) of each traversed node
        discovered = {start_node}               # set of already discovered nodes

        # while stack not empty
        while stack:
            id = int(stack.pop())
            if id in self._nodes:
                # have to iterate over neighbors in reverse order (to pass project tests)
                for n in reversed(self._nodes[int(id)]):
                    # check that the neighbors haven't been already discovered
                    if n not in discovered:
                        stack.append(int(n))    # add the connected node to the queue
                        parent[n] = id          # update parent
                        discovered.add(n)       # indicate this node has been added to the queue
        self._printResults(parent, end_node)


    # perform uniform cost search on the graph
    def UCS(self, start_node, end_node):
        visited = set()                         # set of nodes that have already been popped from the queue
        pq = pqdict({start_node: 0})            # priority queue
        parent = {start_node: None}             # dictionary storing the parent (ID) of each traversed node

        while True:
            try:
                cur_cost = pq[pq.top()]         # cost of reaching this node
                cur = int(pq.pop())             # ID of the current node

                for n in self._nodes[cur]:      # neighbors of current node
                    if n not in visited:
                        # calculate the cost to reach node n
                        n_cost = cur_cost + self._getWeight(cur, n)

                        if n in pq:
                            if n_cost < pq[n]:
                                # cheaper route to node discovered
                                pq[n] = n_cost  # update priority
                                parent[n] = cur # update parent
                        else:
                            pq[n] = n_cost      # add to priority queue
                            parent[n] = cur     # remember how we reached n
                visited.add(cur)                # remember that this node was visited
                if cur == end_node:
                    break

            except KeyError:
                # priority queue is empty
                break
        self._printResults(parent, end_node)


    # prints the final results as an array of node IDs
    def _printResults(self, parent, end_node):
        res = [] # list of the nodes to traverse on the path to the end node
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


    # add an edge to the graph pointing from src node to dest node
    # (this is a directed graph, not bidirectional)
    def _addEdge(self, src, dest):
        if src not in self._nodes:
            self._nodes[src] = []
        self._nodes[src].append(dest)


# command-line arguments
input_file = sys.argv[1]
start_node = int(sys.argv[2])
end_node = int(sys.argv[3])
search_type = sys.argv[4]                       # 'BFS' or 'DFS', or 'UCS'

graph = GraphSearch(input_file)

# search the graph for a path from the start node to the end node
# using the given search type
if search_type == "BFS":
    graph.BFS(start_node, end_node)
if search_type == "DFS":
    graph.DFS(start_node, end_node)
if search_type == "UCS":
    graph.UCS(start_node, end_node)
