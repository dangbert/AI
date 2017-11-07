# Graph Search

### PURPOSE:
To search a directional graph for a target node.

### HOW IT WORKS:
The general purpose decision tree is implemented as a package in the DecisionTree folder.

The proj3.py file is an example usage of the DecisionTree package.  It trains using a large set of data about adults (the adult.data file) and then can classify data points into the income brackets "<=50K" and ">50K"

### HOW TO RUN:
````./Search.py <input_file> <start_node> <end_node> <search_type>````

* input_file: is the filename of a text file defining the graph
* start_node: is the integer (node) to start the search from
* end_node: is the integer (node) that is being searched for

Example input file:
````
1 2 34
2 3 192
3 4 43
4 5 137
````

* The first two numbers on a line represent an edge connecting those two vertices in this graph
  * The first number is that edge's source, and the second number is that edge's destination.
* The third number on a line represents the weight of that edge. This edge is directed from the source to the destination. All three numbers must be integers.

Graph represented by this file:

<img src="https://doc-10-54-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/jp0ffnuvkdl4m3m9uvqdh3cmukmt0g57/1510020000000/13140362715784620068/*/0B1m37QPZw5bTU2pOd1V0ZmRyWms" alt="example graph" width="300">
