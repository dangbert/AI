import math
from copy import deepcopy
#from Kmeans import Tree


# creates a decision tree based on training data
# uses the ID3 algorithm with maximum gain
class Kmeans:

    def train(self, data, labels, k):
        self._data = data
        self._labels = labels
        self._k = k

        #self._createTree()


    def _createTree(self, tree, pAttr, rlist):
        pass


    # classify a vector (after training has been completed)
    def classify(self, x):
        print("in classify")
